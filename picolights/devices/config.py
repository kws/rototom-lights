
from picologger import getLogger

logger = getLogger(__name__)

def as_pin(pin):
    """
    Converts a pin number or name to a pin object. 
    """
    import microcontroller
    if isinstance(pin, microcontroller.Pin):
        return pin
    
    import board
    return getattr(board, pin)

def as_enum(name, value):
    try:
        _package, _class = name.rsplit(".", 1)
        _from_type = [_class]
    except ValueError:
        _package = name
        _class = None
        _from_type = []

    package = __import__(_package, globals(), locals(), _from_type)

    if _class:
        enum = getattr(package, _class)
    else:
        enum = package

    return getattr(enum, value)

def create_microcontroller(controller, **kwargs) -> None:
    from .microcontroller import Microcontroller
    return Microcontroller(controller=controller, **kwargs)


def create_neopixel(controller, count, pin, auto_write=False, animation=None, on_animation=None, off_animation=None, **kwargs) -> None:
    import neopixel
    from picolights.devices.pixelstrip import PixelBufferController
    pixels = neopixel.NeoPixel(as_pin(pin), count, auto_write=auto_write, **kwargs)
    return PixelBufferController(pixels, controller=controller, animation=animation, on_animation=on_animation, off_animation=off_animation)


def create_pixel_subset(controller, ref, start, end, **kwargs) -> None:
    from adafruit_led_animation.helper import PixelSubset
    from picolights.devices.pixelstrip import PixelBufferController
    pixels = PixelSubset(controller[ref].pixels, start, end)
    pixels.bpp = controller[ref].pixels.bpp
    return PixelBufferController(pixels, controller=controller, **kwargs)


def create_pin_out(_, pin, drive_mode=None, **kwargs):
    kwargs = kwargs.copy()
    kwargs["pin"] = as_pin(pin)
    if drive_mode:
        kwargs["drive_mode"] = as_enum("digitalio.DriveMode", drive_mode)
    from .gpio import PinOut
    return PinOut(**kwargs)

def create_pin_in(_, pin, pull=None, **kwargs):
    kwargs = kwargs.copy()
    kwargs["pin"] = as_pin(pin)
    if pull:
        kwargs["pull"] = as_enum("digitalio.Pull", pull)
    from .gpio import PinIn
    return PinIn(**kwargs)

def create_watchdog(_, **kwargs):
    from .watchdog import DeviceWatchdog
    return DeviceWatchdog(**kwargs)

def create_mqtt_watchdog(_, **kwargs):
    from .watchdog import MQTTWatchdog
    return MQTTWatchdog(**kwargs)

def create_generic(device_type):
    package, class_name = device_type.rsplit(".", 1)
    module = __import__(package, globals(), locals(), [class_name])
    constructor = getattr(module, class_name)
    def factory(_, *args, **kwargs):
        print("Creating generic device", device_type, args, kwargs)
        return constructor(*args, **kwargs)
    return factory

class _DeviceFactory:

    def __init__(self):
        self.__device_types = {}
        self.__device_types["microcontroller"] = create_microcontroller
        self.__device_types["neopixel"] = create_neopixel
        self.__device_types["pixel-subset"] = create_pixel_subset
        self.__device_types["pin-out"] = create_pin_out
        self.__device_types["relay"] = create_pin_out # alias
        self.__device_types["pin-in"] = create_pin_in
        self.__device_types["watchdog"] = create_watchdog
        self.__device_types["mqtt-watchdog"] = create_mqtt_watchdog
        self.__device_types["ow-temp"] = create_generic("picolights.devices.ow_temp.OwTemp")
        self.__device_types["ldr"] = create_generic("picolights.devices.ldr.LDR")
        self.__device_types["keypad"] = create_generic("picolights.devices.keypad.Keypad")


    def __getitem__(self, key):
        return self.__device_types[key]
    
    def __contains__(self, key):
        return key in self.__device_types
    
    def register(self, name, factory):
        self.__device_types[name] = factory


device_factory = _DeviceFactory()


class DeviceList:
    
    def __init__(self, devices):
        self.__devices = {}

        if not devices:
            logger.warning("No devices configured")
            return
        
        for device in devices:
            try:
                self.__register_device(device)
            except Exception as ex:
                logger.error(f"Error creating device %s: %s", device, ex)

    def __register_device(self, device):
        device_type = device.pop("type")
        device_id = device.pop("id")

        if "." in device_type:
            package, class_name = device_type.rsplit(".", 1)
            module = __import__(package, globals(), locals(), [class_name])
            factory = getattr(module, class_name)
        else:
            factory = device_factory[device_type]
        self.__devices[device_id] = device = factory(self, **device)
        setattr(device, 'device_name', device_id)

    def __getitem__(self, key):
        return self.__devices[key]
    
    def __iter__(self):
        return iter(self.__devices.items())
    
    def loop(self):
        for device in self.__devices.values():
            try:
                device.loop()
            except AttributeError:
                pass
            except Exception as ex:
                logger.error(f"Error in device loop: {ex}")


