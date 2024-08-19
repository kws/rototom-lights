import time
from picolights.devices.controller import PropertyManager
from picologger import getLogger
import microcontroller
logger = getLogger(__name__)


class DeviceWatchdog:
    from watchdog import WatchDogMode

    def __init__(self, mode=WatchDogMode.RESET, timeout=8.3, start_delay=30):
        self.w = None
        self.mode = mode
        self.timeout = timeout
        self.start_time = time.monotonic() + start_delay

    def init_watchdog(self):
        if self.w is None:
            # logger.info("Starting watchdog")
            from microcontroller import watchdog as w
            w.mode = self.mode
            w.timeout = self.timeout
            self.w = w
        return self.w

    def loop(self):
        if time.monotonic() < self.start_time:
            return
        print("Feeding watchdog")
        w = self.init_watchdog()
        w.feed()


class MQTTWatchdog:

    def __init__(self, start_delay=10, ping_interval=60, timeout_interval=300):
        from smartdev.cpu import short_mac, ipv4

        # Special variables
        self.message_bus = None
        self.property_manager = PropertyManager(self, ["ping"])

        # Config variables
        self.device_name = None
        self.ping_interval = ping_interval
        self.timeout_interval = timeout_interval
        self.last_ping_sent = 0
        self.last_ping_received = time.monotonic()
        self.device_id = short_mac()
        self.start_time = time.monotonic() + start_delay
        self.ipv4 = ipv4

    @property
    def ping(self):
        return None
    
    @ping.setter
    def ping(self, msg):
        self.last_ping_received = time.monotonic()
        logger.info("Ping received")
 
    def __send_ping(self):
        try:
            message = f"This is a ping from {self.device_id} on {self.ipv4()} with time {time.monotonic()}"
        except:
            message = "This is the fallback ping - something is not working"
        print("Sending ping message")
        self.message_bus.publish(f"{self.device_name}/ping/set", message)
        self.last_ping_sent = time.monotonic()

    def loop(self):
        if time.monotonic() < self.start_time:
            return
            
        if time.monotonic() - self.last_ping_sent > self.ping_interval:
            self.__send_ping()

        if time.monotonic() - self.last_ping_received > self.timeout_interval:
            logger.error("MQTT watchdog timed out")
            microcontroller.reset()


