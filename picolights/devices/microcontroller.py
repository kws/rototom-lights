import microcontroller
import time
import gc

from picolights.devices.controller import PropertyManager

class Microcontroller:

    def __init__(self, controller, update_interval=300, gc=None):
        self._controller = controller
        self.property_manager = PropertyManager(self,  [
                "reset", "uptime", "temperature", "voltage", "frequency", "memory", "update_interval",
                "ip", "mac", "hostname", "cpu_id"
            ])
        self.update_interval = update_interval

        if gc:
            self.memory = gc

    @property
    def reset(self):
        return "OFF"

    @reset.setter
    def reset(self, message):
        microcontroller.reset()

    @property
    def ip(self):
        try:
            import wifi
            return wifi.radio.ipv4_address
        except:
            return None
        
    @property
    def mac(self):
        try:
            import wifi
            return ":".join(["%02x" % b for b in wifi.radio.mac_address])
        except:
            return None

    @property
    def cpu_id(self):
        try:
            from smartdev import cpu
            return cpu.short_mac()
        except:
            return None
        
    @property
    def hostname(self):
        try:
            import wifi
            return wifi.radio.hostname
        except:
            return None

    @property
    def uptime(self):
        return f"{time.monotonic():.0f}"
    
    @property
    def temperature(self):
        if microcontroller.cpu.temperature:
            return f"{microcontroller.cpu.temperature:.1f}"
        else:
            return ""
    
    @property
    def voltage(self):
        if microcontroller.cpu.voltage:
            return f"{microcontroller.cpu.voltage:.2f}"
        else:
            return ""
    
    @property
    def frequency(self):
        return microcontroller.cpu.frequency
    
    @property
    def memory(self):
        return gc.mem_free()
    
    @memory.setter
    def memory(self, value):
        if value == "on": 
            gc.enable()
        elif value == "off":
            gc.disable()
        else:
            gc.collect()
        self.property_manager.update("memory")
    
    @property
    def update_interval(self):
        return self._update_interval
    
    @update_interval.setter
    def update_interval(self, value):
        self._update_interval = float(value)
        self._last_update = 0
        self.property_manager.update("update_interval")
    
    def loop(self):
        if time.monotonic() - self._last_update > self._update_interval:
            self._last_update = time.monotonic()
            self.property_manager.update_all()
