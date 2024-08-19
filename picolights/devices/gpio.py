from digitalio import DriveMode, DigitalInOut
from picolights.devices.controller import PropertyManager


class PinOut:

    __managed_props__ = ["switch"]

    def __init__(self, pin, value=False, drive_mode=DriveMode.PUSH_PULL, inverted=False):
        self.property_manager = PropertyManager(self,  ["switch"])

        self.pin = DigitalInOut(pin)
        self.pin.switch_to_output(value=value, drive_mode=drive_mode)
        self.inverted = inverted        

    @property
    def switch(self):
        return self.pin.value ^ self.inverted
    
    @switch.setter
    def switch(self, message):
        if isinstance(message, bool):
            status = message
        else:
            status = str(message).lower() in ("on", "true", "1")

        self.pin.value = status  ^ self.inverted


class PinIn:

    def __init__(self, pin, inverted=False, pull=None):
        self.property_manager = PropertyManager(self,  ["switch"])

        self.pin = DigitalInOut(pin)
        self.pin.switch_to_input(pull)
        self.inverted = inverted

    @property
    def switch(self):
        return self.pin.value ^ self.inverted
