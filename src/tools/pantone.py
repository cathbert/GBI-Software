import json

import asyncio

import math

# db = Database()

def loadPantoneColors():
    with open("src/tools/pantone_colors.json", "r") as f:
        pantone_colors = json.load(f)
    return pantone_colors

async def loadPantoneColorsHex():
    with open("src/tools/pantone_colors.json", "r") as f:
        pantone_colors = json.load(f)
    return [loadPantoneColors()[i]['hex'] for i in pantone_colors]

async def searchPantoneUsingHex(hex_color):
    pantone_colors = await loadPantoneColorsHex()
    if hex_color in pantone_colors:
        return loadPantoneColors()[hex_color]
    else:
        return await searchPantoneColorUsingHex(hex_color)
    
async def searchPantoneColorUsingHex(hex_color):
    pantone_colors = await loadPantoneColorsHex()
    color_distance_list = []

    input_color = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    for i in range (len(pantone_colors)):
        use_color = pantone_colors[i]
        my_color = tuple(int(use_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        get_distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(my_color, input_color)])) 
        color_distance_list.append(get_distance)

    sorted_color_distance_list = min(color_distance_list)
    closest_hex = color_distance_list.index(sorted_color_distance_list)

    return pantone_colors[closest_hex]


# print(asyncio.run(loadPantoneColorsHex()))
# asyncio.run(searchPantoneColorUsingHex("#f2ab46"))
# for i in loadPantoneColors():
#     print(i)
#     loadPantoneColors()[i]
#     print(loadPantoneColors()[i])
#     db.addPantone(i, loadPantoneColors()[i]['name'], loadPantoneColors()[i]['hex'])
    