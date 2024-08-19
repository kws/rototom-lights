def blend_colors(A, B, t):
    """Blend two RGB colors using factor t.
    
    Args:
    A, B: Tuple of (R, G, B) where each value is in [0, 255].
    t: Blend factor. When t=0, the result is A. When t=1, the result is B.

    Returns:
    Tuple of (R, G, B) representing the blended color.
    """
    if len(A) == 3:
        return (
            int((1 - t) * A[0] + t * B[0]),
            int((1 - t) * A[1] + t * B[1]),
            int((1 - t) * A[2] + t * B[2])
        )
    else:
        return (
            int((1 - t) * A[0] + t * B[0]),
            int((1 - t) * A[1] + t * B[1]),
            int((1 - t) * A[2] + t * B[2]),
            int((1 - t) * A[3] + t * B[3])
        )

def blend_two_colours(A, B):    
    if len(A) == 3:
        return (
            ((A[0] & 0xFE) + (B[0] & 0xFE)) >> 1,
            ((A[1] & 0xFE) + (B[1] & 0xFE)) >> 1,
            ((A[2] & 0xFE) + (B[2] & 0xFE)) >> 1
        )
    else:
        return (
            ((A[0] & 0xFE) + (B[0] & 0xFE)) >> 1,
            ((A[1] & 0xFE) + (B[1] & 0xFE)) >> 1,
            ((A[2] & 0xFE) + (B[2] & 0xFE)) >> 1,
            ((A[3] & 0xFE) + (B[3] & 0xFE)) >> 1 
        )

def naive_blend(A, B):    
    if len(A) == 3:
        return (
            max(A[0], B[0]),
            max(A[1], B[1]),
            max(A[2], B[2])
        )
    else:
        return (
            max(A[0], B[0]),
            max(A[1], B[1]),
            max(A[2], B[2]),
            max(A[3], B[3])
        )

class BlendStrip:
    """
    Emulates a list of pixels, but every set call blends the color with the previous color. Each blend 
    contributes a little bit less so that all colours shoudl be equally represented.

    The first draw does not blend with the 'initial_color'.
    """
    def __init__(self, length, initial_color=(0, 0, 0)):
        self._pixels = [initial_color] * length
        self._draw_counts = [0] * length

    def __len__(self):
        return len(self._pixels)
    
    def __getitem__(self, key):
        return self._pixels[key]
    
    def __setitem__(self, key, value):
        if self._draw_counts[key] == 0:
            self._pixels[key] = value
        else:
            # self._pixels[key] = blend_colors(self._pixels[key], value, 1 / (self._draw_counts[key] + 1))
            self._pixels[key] = naive_blend(self._pixels[key], value)
        self._draw_counts[key] += 1
