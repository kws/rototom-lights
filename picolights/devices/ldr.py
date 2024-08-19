from collections import deque
from picolights.devices.controller import PropertyManager
from picologger import getLogger
import analogio
import time

logger = getLogger(__name__)

e = 2.718


def reading_to_voltate(reading):
    return 3.3 * reading / 65535

def voltage_to_lux(voltage):
    if voltage <= 2.5:
        # return (106.88 * voltage) - 23.7
        return 100 * voltage
    else:
        return 0.03 * (e ** (3.57 * voltage)) 


class LDR:
    """
    Light dependend resistor
    """

    def __init__(self, pin, update_interval=1, measurements=100, rounding=25):
        from .config import as_pin
        pin = as_pin(pin)
        self.__sensor = analogio.AnalogIn(pin)
        self.__rounding = rounding
        self.property_manager = PropertyManager(self, ["voltage", "lux"])
        self.measurements = deque(tuple(), measurements)

        self.update_interval = update_interval
        self.__next_update = 0

        self._update()


    def _update(self):
        measurement_length = len(self.measurements)
        if measurement_length:
            self.reading = sum([self.measurements.popleft() for _ in range(measurement_length)]) / measurement_length
        else:
            self.reading = self.__sensor.value
        voltage = reading_to_voltate(self.reading)
        lux = voltage_to_lux(voltage)

        self.voltage = f"{voltage:.1f}"
        self.lux = int(lux/self.__rounding) * self.__rounding 
        self.property_manager.update()


    def loop(self):
        self.measurements.append(self.__sensor.value)
        if time.monotonic() > self.__next_update:
            self._update()
            self.__next_update = time.monotonic() + self.update_interval
