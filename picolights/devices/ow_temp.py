import adafruit_ds18x20
from picolights.devices.controller import PropertyManager
from adafruit_onewire.bus import OneWireBus
from picologger import getLogger
from binascii import hexlify

logger = getLogger(__name__)

class OwTemp:

    def __init__(self, pin, ow_devices):
        from .config import as_pin
        pin = as_pin(pin)
        logger.info(f"ONEWIRE PIN: {pin}")

        self.device_name_to_serial = ow_devices
        self.device_serial_to_name = {v: k for k, v in ow_devices.items()}
        self.expect_device_count = len(ow_devices)
        self.devices = {}

        self.property_manager = PropertyManager(self, [n for n in ow_devices.keys()])
        for prop in self.property_manager.props:
            setattr(self, prop, "Not Found")

        self.ow_bus = OneWireBus(pin)
        self.scan_devices()

    def scan_devices(self):
        ow_devices = self.ow_bus.scan()
        if len(ow_devices) == self.expect_device_count:
            logger.info(f"ONEWIRE TEMP: Found {len(ow_devices)} devices")
        else:
            logger.warning(f"ONEWIRE TEMP: Found {len(ow_devices)} devices, expected {self.expect_device_count}")
        for d in ow_devices:
            serial = hexlify(d.serial_number).decode("utf-8").upper()
            name = self.device_serial_to_name.get(serial)
            if name:
                ds18b20 = adafruit_ds18x20.DS18X20(self.ow_bus, d)
                self.devices[name] = ds18b20
                print(f"Found DS18B20 '{name}' with serial {serial}")

    def loop(self):
        if self.expect_device_count is not None:
            if len(self.devices) != self.expect_device_count:
                self.scan_devices()
        for name, ds18b20 in self.devices.items():
            try:
                setattr(self, name, f"{ds18b20.temperature:0.1f}")
            except Exception:
                pass
        self.property_manager.update(*self.property_manager.props)
        

