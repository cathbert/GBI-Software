import webcolors
import matplotlib.pyplot as plt
import colorsys

# print(webcolors.hex_to_name("#6ab123"))

def closest_color(rgb_color):
    min_colours = {}
    for name in webcolors.names("css3"):
        r_c, g_c, b_c = webcolors.name_to_rgb(name)
        rd = (r_c - rgb_color[0]) ** 2
        gd = (g_c - rgb_color[1]) ** 2
        bd = (b_c - rgb_color[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

print(closest_color((0, 0, 255)))    