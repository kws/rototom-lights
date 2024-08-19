import random
from picolights.colors import rgb_to_hsv, hsv_to_rgb, to_color
from picolights.effects.helpers import PicoAnimation


def adjust_value(value, target_value=0.5, max_step=0.1, random_weight=3):
    dist_from_target = abs(value - target_value)
    # Increase weight with distance
    weight = dist_from_target
    # Determine the direction towards the target
    direction = 1 if value < target_value else -1
    # Calculate step
    # step = direction * random.random() * max_step * weight
    # Adding additional randomness
    random_factor = random.random()
    # Calculate step with additional randomness
    step = direction * random_factor * max_step * (weight + random_factor * random_weight)

    # Update value
    value = value + step
    return max(0, min(1, value))


class Starlight(PicoAnimation):

    def __init__(self, pixel_object, pixel_probability=0.1, target_saturation=0.5, target_value=0.5):
        super().__init__(pixel_object)

        self.pixel_probability = pixel_probability
        self.target_saturation = target_saturation
        self.target_value = target_value

    def draw(self):
        for p in range(len(self.pixel_object)):
            if random.random() < self.pixel_probability:
                current_color = self.pixel_object[p]
                current_color = to_color(current_color)
                h, s, v = rgb_to_hsv(*current_color)
                s = adjust_value(s, self.target_saturation)
                v = adjust_value(v, self.target_value)
                h = h + (random.random() - 0.5) * 360
                
                self.pixel_object[p] = hsv_to_rgb(h, s, v)


    def __str__(self) -> str:
        str = f"starlight pixel_probability={self.pixel_probability} target_saturation={self.target_saturation} target_value={self.target_value}"
        return str