import analogio
import board
from digitalio import DriveMode, DigitalInOut
import time
import keypad
from picolights.devices.controller import PropertyManager


class Keypad:

    __managed_props__ = ["switch"]

    def __init__(self, keymapping, value_when_pressed=True, pull=True):
        keymapping = [(v, getattr(board, k)) for k, v in keymapping.items()]

        self._keymapping = keymapping
        self._keypad = keypad.Keys([k[1] for k in keymapping], value_when_pressed=value_when_pressed, pull=pull)
        self.property_manager = PropertyManager(self,  [k[0] for k in keymapping])
        for k in keymapping:
            self.property_manager.set(k[0], "OFF")

    def loop(self):
        ev = self._keypad.events.get()
        if ev:
            key = self._keymapping[ev.key_number]
            value = "ON" if ev.pressed else "OFF"
            if getattr(self, key[0]) != value:
                self.property_manager.set(key[0], value)
                self.property_manager.update(key[0])
            print(ev, ev.pressed, key)
            print("SENT")

