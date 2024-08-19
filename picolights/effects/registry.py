from .helpers import PicoAnimation
from .transition import Transition
from adafruit_logging import getLogger

logger = getLogger(__name__)

class AnimationRegistry:

    def __init__(self) -> None:
        self.animations = {}

    def _get_class(self, package, class_name):
        try:
            module = __import__(package, globals(), locals(), [class_name])
        except ImportError:
            return None
        return getattr(module, class_name)

    def get_animation(self, name):
        if "." in name:
            name, class_name = name.rsplit(".", 1)
            return self._get_class(name, class_name)

        name = name.strip().lower()
        uppercase_name = name[0].upper() + name[1:]

        # Try local
        animation = self._get_class(f"picolights.effects.animations.{name}", uppercase_name)
        if animation:
            return animation 
        
        # Try standard
        animation = self._get_class(f"adafruit_led_animation.animation.{name}", uppercase_name)
        return animation 


animation_register = AnimationRegistry()


def create_animation(pixels, message):
    if message[0] == "{":
        import json
        config = json.loads(message)
        animation = config.pop("name").lower()
        args = []
    else:
        tokens = message.split(" ")
        animation = tokens[0].lower()
        args = []
        config = {}
        if len(tokens) > 1:
            tokens = tokens[1:]
            for token in tokens:
                if token == "":
                    continue
                elif "=" in tokens[0]:
                    key, value = token.split("=", 1)
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                    config[key] = value
                else:
                    args.append(token)

    animation_class = animation_register.get_animation(animation)
    if not animation_class:
        logger.error("Animation %s not found", animation)
        return None
    
    transition = config.pop("transition", None)
    transition_duration = config.pop("transition_duration", 0.5)
    transition_easing = config.pop("transition_easing", None)

    if transition:
        pixels = Transition(pixels, transition=transition, duration=transition_duration, easing=transition_easing)

    animation = None
    if hasattr(animation_class, "create_animation"):
        animation = animation_class.create_animation(pixels, *args, **config)
    elif not isinstance(animation_class, PicoAnimation):
        animation = animation_class(pixels, **config)
        
    return animation
