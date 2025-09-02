import flet as ft
import glob
import random
import string
import re
from dateutil import parser
import segno
from PIL import Image
# import EAN13 from barcode module
from barcode import EAN13

# import ImageWriter to generate an image file
from barcode.writer import ImageWriter


def teeImages():
    
    garment_names = [i.lstrip("src\\assets\\garments-images\\").rstrip(".png") for i in glob.glob("src\\assets\\garments-images\\*.png")]
    garment_paths = glob.glob("src\\assets\\garments-images\\*.png")

    return list(zip(garment_names, garment_paths))
# print(teeImages())
# for i in glob.glob("src\\assets\\garments-images\\*.png"):
#     print(i.lstrip("src\\assets\\garments-images\\").rstrip(".png"))

def seacrchColorGarment(text: str):
    garments=[]
    for n, p in teeImages():
        if text.lower() in n.lower():
            garments.append((n, p))
        else:
            pass
    return garments

def generate_order_number():
    order_no = []
    for i in range(3):
        order_no.append(random.choice([i for i in string.digits]))
    for n in range(4):
        order_no.append(random.choice([i for i in string.ascii_uppercase]))
    return "GBI"+"".join(order_no)


def convertdate(date_time):
    date_time = parser.parse(date_time)
    return date_time.strftime("%A %d/%m/%Y - %I %S%p")

def convertdateonly(date_time):
    date_time = parser.parse(date_time)
    return date_time.strftime("%A %d/%m/%Y")

def converttime(date_time):
    date_time = parser.parse(date_time)
    return date_time.strftime("%I:%S%p")

def verifyPhoneNumber(no):
    if len(no) == 10 and no.isnumeric():
        return True
    else:
        return False

def validateEmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    valid = re.match(pattern, email)
    return True if valid else False

def generateEmail(name, phone):
    return name+"_"+phone+"@gbinks.com"

def qrcodeGenerator(code):
    qrcode = segno.make_qr(code)
    qrcode.save(
        f"src/reports/codes/{code}.png", 
        scale=5,
        border=2
        # light="lightblue",
    )
    

def barCodeGenerator(code):
    # Now, let's create an object of EAN13 class and 
    # pass the number with the ImageWriter() as the 
    # writer
    my_code = EAN13(code, writer=ImageWriter())

    # Our barcode is ready. Let's save it.
    my_code.save(f"src/reports/barcodes/{code}")

def createWaterMark(img):
    img = Image.open(img)
    img.putalpha(127) # Half alpha; alpha argument must be an int
    img.save("src/reports/GBI-LOGO.png")

# createWaterMark("src/assets/GBI-LOGO.png")

# barCodeGenerator("7483829401274")
# qrcodeGenerator("84774783")
# print(verifyPhoneNumber("8788847740"))
# print(validateEmail("cmutaurwa@gmail.com"))