from picologger import getLogger
import time

logger = getLogger(__name__)

class PropertyManager:

    def __init__(self, device, props):
        self.device = device
        self.props = props
        self.device_name = None
        self.message_bus = None
        self.__last_properties = {}

    def initialise(self, device_name, message_bus):
        logger.info("Initializing device %s with properties: %s", device_name, self.props)
        self.device_name = device_name
        self.message_bus = message_bus
        self.update(*self.props)

    def set(self, prop, value):
        if prop not in self.props:
            logger.error("Unknown property: %s", prop)
            return
        setattr(self.device, prop, value)

    def update(self, *prop_list):
        if not prop_list:
            prop_list = self.props
        for prop in prop_list:
            if prop not in self.props:
                logger.error("Unknown property: %s", prop)
                continue
            
            value = getattr(self.device, prop, None)
            if value != self.__last_properties.get(prop, None):
                logger.info("Property changed: %s.%s = %s", self.device_name, prop, value)
                self.__last_properties[prop] = value
                if self.message_bus:
                    self.message_bus.publish(f"{self.device_name}/{prop}", value)

    def update_all(self):
        self.update(*self.props)

class DeviceController:

    def __init__(self, device_list, message_bus):
        self.__device_list = device_list
        self.__message_bus = message_bus
        self.__next = 0

        for device_name, device in self.__device_list:
            property_manager = getattr(device, "property_manager", None)
            if property_manager:
                property_manager.initialise(device_name, message_bus)

            if hasattr(device, "message_bus"):
                device.message_bus = message_bus

        message_bus.subscribe(f"#", self.__on_message)

    def __on_message(self, client, topic, message):
        logger.info("Received message from %s: %s = %s", client, topic, message)
        topic_parts = topic.split("/")
        if not len(topic_parts) == 3 or topic_parts[2] != "set": # Not a setter topic
            return

        device_name, prop, _ = topic_parts

        try:
            device = self.__device_list[device_name]
        except KeyError:
            logger.error("Unknown device: %s", device_name)
            return 
        
        try:
            device.property_manager.set(prop, message.strip())
        except Exception as e:
            logger.exception("Error setting property %s.%s", device_name, prop, exception=e)
            return
        
        logger.info("Set property: %s.%s = %s", device_name, prop, message)

        
    def __announce(self):
        device_names = [d[0] for d in self.__device_list]
        logger.info("Announcing devices: %s", device_names)
        self.__message_bus.publish("devices", ", ".join(device_names), retain=True)
    

    def loop(self):
        if time.monotonic() > self.__next:
            self.__next = time.monotonic() + 30*60 # Announce every 30 minutes
            self.__announce()

