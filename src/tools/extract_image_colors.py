from colorthief import ColorThief
from PIL import Image
import matplotlib.pyplot as plt
import colorsys


ct = ColorThief('src/tools/test_image.jpg')
# print(ct.get_palette(color_count=6))
# print(ct.get_color(quality=1))

# dorminent_color = ct.get_color(quality=1)
# plt.imshow([[dorminent_color]])
# plt.axis('off')  # Turn off axis numbers and ticks
# plt.show()

palette = ct.get_palette(color_count=6)
# plt.imshow([[palette[i] for i in range(len(palette))]])
# plt.axis('off')  # Turn off axis numbers and ticks
# plt.show()

def color_to_hex(color):
    return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

# colorsys.rgb_to_hsv(255, 0, 0)
def color_to_hsv(color):
    r, g, b = color
    return colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

def color_to_hsl(color):
    r, g, b = color
    return colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)

def color_to_cmyk(color):
    r, g, b = color
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 100
    c = 1 - r / 255.0
    m = 1 - g / 255.0
    y = 1 - b / 255.0
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy
    return int(c * 100), int(m * 100), int(y * 100), int(k * 100)

def hls_to_rgb(h, l, s):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)

def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)

for color in palette:
    print(f"{color} {color_to_hex(color)}")