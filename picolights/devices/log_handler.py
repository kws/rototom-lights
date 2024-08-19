

from picolights.devices.config import as_enum
from picolights.colors import to_color
from picologger import getLogger, getRootLogger, INFO, Handler
import time


        # log_pixels = device.pop("log_pixels", None)
        # if isinstance(log_pixels, str):
        #     log_pixels = [int(x) for x in log_pixels.split("-")]
        # elif isinstance(log_pixels, int):
        #     log_pixels = [log_pixels, log_pixels+1]

        # if log_pixels:
        #     self.__log_devices.append((self.__devices[device_id], log_pixels))


    # def set_log_color(self, color=None):
    #     if color:
    #         from ..colors import to_color
    #         self.__log_handler.color = to_color(color)
    #         self.__root_logger.addHandler(self.__log_handler)
    #     else:
    #         self.__root_logger.removeHandler(self.__log_handler)
    



class DeviceLogHandler(Handler):
    """
    We can flash some pixels when a log message is received.
    """

    def __init__(self, device_list, device, level="debug", color="green", start_pixel=0):
        level = as_enum("picologger", level.upper())
        super().__init__(level)
        self.color = to_color(color)
        self.device = device_list[device]
        self.start_pixel = start_pixel

    def _fill(self, color):
        for device, ix in self.__device_list:
            for i in range(ix[0], ix[1]):
                device.pixels[i] = color
            device.pixels.show()


    def emit(self, record) -> None:
        if not self.color:
            return

        if sum(self.device.pixels[self.start_pixel]):
            self.device.pixels[self.start_pixel] = 0
        else:
            self.device.pixels[self.start_pixel] = self.color
        self.device.pixels.show()

