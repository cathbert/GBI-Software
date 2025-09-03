import json
from database import Database

db = Database()

def loadPantoneColors():
    with open("src/tools/pantone_colors.json", "r") as f:
        pantone_colors = json.load(f)
    return pantone_colors

# for i in loadPantoneColors():
#     print(i)
#     loadPantoneColors()[i]
#     print(loadPantoneColors()[i])
#     db.addPantone(i, loadPantoneColors()[i]['name'], loadPantoneColors()[i]['hex'])
    