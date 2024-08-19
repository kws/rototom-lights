from binascii import unhexlify
import json
from picologger import getLogger

logger = getLogger(__name__)

__block_pos = []
__name_cache = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "white": (255, 255, 255),
    "warmwhite": (255, 147, 41),
    "black": (0, 0, 0),
}


def __index_colors():
    """
    Indexes the colors.txt file
    """
    global __block_pos

    try:
        with open("picolights/colors/color_index.json", "rt") as f:
            __block_pos = json.load(f)
        return
    except:
        pass

    with open("picolights/colors/colors.txt", "rt") as f:
        last_start = None
        index_next = True

        while c := f.read(1):
            if index_next:
                index_next = False
                if c != last_start:
                    last_start = c
                    __block_pos.append(f.tell())
            if c == "\n":
                index_next = True
        __block_pos.append(f.tell())

def from_color_name(name: str) -> str:
    """
    Caches name lookups to speed up future lookups
    """
    if name in __name_cache:
        return __name_cache[name]
    color = lookup_color_name(name)
    __name_cache[name] = color
    return color

def lookup_color_name(name: str) -> str:
    """
    Looks up hex value from color name
    """
    if name is None:
        return None

    if not __block_pos:
        __index_colors()
    name = name.lower().strip()
 
    v = name[0]
    pos = ord(v[0])-97
    start = __block_pos[pos]
    end = __block_pos[pos+1] 
 
    with open("picolights/colors/colors.txt", "rt") as f:
        if start > 0:
            f.seek(start-1)
        val = f.read(end-start)
        for line in val.splitlines():
            color, hex = line.rsplit("#", 1)
            if color.strip() == name:
                return int.from_bytes(unhexlify(hex.strip()), "big")

if __name__ == "__main__":
    __index_colors()
    with open("picolights/colors/color_index.json", "wt") as f:
        json.dump(__block_pos, f)
    print("Wrote color index to color_index.json")