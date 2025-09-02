from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from controller import qrcodeGenerator, barCodeGenerator
import os
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import datetime
from controller import convertdateonly, converttime


pdfmetrics.registerFont(TTFont("RobotoBold", "src/assets/fonts/Roboto-Bold.ttf"))
pdfmetrics.registerFont(TTFont("RobotoLight", "src/assets/fonts/Roboto-Light.ttf"))
pdfmetrics.registerFont(TTFont("RobotoSemiBold", "src/assets/fonts/Roboto_Condensed-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("RobotoBoldItalic", "src/assets/fonts/Roboto-SemiBoldItalic.ttf"))


class Report(canvas.Canvas):
    def __init__(self, order_ref, client_name, client_contact, client_email, client_address, order_date):
        self.order_ref = order_ref
        self.client_name = client_name
        self.client_contact = client_contact
        self.client_email = client_email
        self.client_address = client_address
        self.order_date = order_date

        super().__init__(filename=f"src/reports/{self.order_ref}.pdf", pagesize=A4)
        self.w, self.h = A4
        print(A4)

        qrcodeGenerator(self.order_ref)
        barCodeGenerator("1198198306041")

        # Watermark
        self.drawImage("src/reports/watermark.png", 50, self.h - 700, width=500, height=500, mask="auto")

        self.drawImage(f"src/reports/codes/{self.order_ref}.png", 50, self.h - 120, width=80, height=80, mask="auto")
        codelabel = self.beginText(55, self.h - 130)
        codelabel.setFont("RobotoBold", 14)
        codelabel.textLine(self.order_ref)
        self.drawText(codelabel)

        self.drawImage("src/assets/GrumpyBearInks.png", 450, self.h - 140, width=100, height=100, mask="auto")
        self.drawImage(f"src/reports/barcodes/1198198306041.png", 40, self.h - 820, width=140, height=65, mask="auto")
        
        self.stamp("deposit")

        label = self.beginText(50, self.h - 180)
        label.setFont("RobotoBold", 14)
        label.textLine("Client Details")
        self.drawText(label)

        datelabel = self.beginText(400, self.h - 180)
        datelabel.setFont("RobotoBold", 14)
        datelabel.textLine("Date:")
        self.drawText(datelabel)

        date = self.beginText(440, self.h - 180)
        date.setFont("RobotoLight", 10)
        date.textLine(convertdateonly(self.order_date))
        self.drawText(date)

        timelabel = self.beginText(400, self.h - 200)
        timelabel.setFont("RobotoBold", 14)
        timelabel.textLine("Time:")
        self.drawText(timelabel)

        time = self.beginText(440, self.h - 200)
        time.setFont("RobotoLight", 10)
        time.textLine(converttime(self.order_date))
        self.drawText(time)

        text = self.beginText(50, self.h - 200)
        text.setFont("RobotoLight", 12)
        text.textLine(f"Name")
        text.textLine(f"Phone")
        text.textLine(f"Email")
        text.textLine(f"Address")
        self.drawText(text)

        self.addClientInfo()

        # Draw a horizontal line Divider.
        x = 50
        y = self.h - 260
        self.line(x, y, x + 500, y)

        itemlabel = self.beginText(50, self.h - 280)
        itemlabel.setFont("RobotoBold", 14)
        itemlabel.textLine("Items")
        self.drawText(itemlabel)

        qtylabel = self.beginText(160, self.h - 280)
        qtylabel.setFont("RobotoBold", 14)
        qtylabel.textLine("Qty")
        self.drawText(qtylabel)

        descriptionlabel = self.beginText(200, self.h - 280)
        descriptionlabel.setFont("RobotoBold", 14)
        descriptionlabel.textLine("Description")
        self.drawText(descriptionlabel)

        colorslabel = self.beginText(400, self.h - 280)
        colorslabel.setFont("RobotoBold", 14)
        colorslabel.textLine("Colors")
        self.drawText(colorslabel)

        # Draw a vertical line Divider.
        x = 460
        y = self.h - 260
        self.line(x1=x, y1=y, x2=460, y2=self.h - 710)

        amountlabel = self.beginText(480, self.h - 280)
        amountlabel.setFont("RobotoBold", 14)
        amountlabel.textLine("Amount(R)")
        self.drawText(amountlabel)

        for i in range(0,60, 20):
            self.__addItem(i)

        # Draw a horizontal line Divider.
        x = 50
        y = self.h - 290
        self.line(x, y, x + 500, y)

        # Draw a horizontal line Bottom Divider.
        x = 50
        y = self.h - 670
        self.line(x, y, x + 500, y)

        summary_label = self.beginText(50, self.h - 690)    
        summary_label.setFont("RobotoBold", 14)
        summary_label.textLine("Summary:")
        self.drawText(summary_label)

        summary = self.beginText(80, self.h - 710)    
        summary.setFont("RobotoLight", 12)
        summary.textLines("Items : 3 Quantity : 30")
        self.drawText(summary)

        total_label = self.beginText(400, self.h - 690)
        total_label.setFont("RobotoBold", 14)
        total_label.textLine("Total:")
        self.drawText(total_label)

        total = self.beginText(480, self.h - 690)
        total.setFont("RobotoBold", 14)
        total.textLine("300.00")
        self.drawText(total)


        contacts = self.beginText(340, self.h - 780)
        contacts.setFont("RobotoBoldItalic", 14)
        contacts.textLines("Email: grumpybearinks@gmail.com\nCall/Whatsapp: 076 749 2077")
        self.drawText(contacts)
        
        
        self.save()
        os.remove(f"src/reports/codes/{self.order_ref}.png")

    def stamp(self, status):
        if status == 'paid':
            self.drawImage(f"src/reports/FULLY-PAID-STAMP.png", 160, self.h - 800, width=140, height=115, mask="auto")
        elif status == 'deposit':
            self.drawImage(f"src/reports/DEPOSIT-PAID-STAMP.png", 160, self.h - 800, width=140, height=115, mask="auto")
    def addClientInfo(self):
        text = self.beginText(100, self.h - 200)
        text.setFont("RobotoSemiBold", 12)
        text.textLine(f":  {self.client_name}")
        text.textLine(f":  {self.client_contact}")
        text.textLine(f":  {self.client_email}")
        text.textLine(f":  {self.client_address}")
        self.drawText(text)

    def __addItem(self, adder):
        tet = 350
        item = self.beginText(50, self.h - tet + adder)
        item.setFont("RobotoLight", 12)
        item.textLine("Product")
        self.drawText(item)

        qty = self.beginText(160, self.h - tet + adder)
        qty.setFont("RobotoLight", 12)
        qty.textLine("10")
        self.drawText(qty)

        desc = self.beginText(200, self.h - tet + adder)
        desc.setFont("RobotoLight", 12)
        desc.textLine("This is an awesome description")
        self.drawText(desc)

        colors = self.beginText(400, self.h - tet + adder)
        colors.setFont("RobotoLight", 12)
        colors.textLine("3")
        self.drawText(colors)

        amount = self.beginText(480, self.h - tet + adder)
        amount.setFont("RobotoLight", 12)
        amount.textLine("100.00")
        self.drawText(amount)


# receipt = Report(order_ref="GBI-84774783", 
#                  client_name="Cathbert", 
#                  client_contact="0736745634",
#                  client_email='cmutaurwa@gbinks.com', 
#                  client_address="1198 Chitown",
#                  order_date="2025-08-23 19:52:27.196260"),


# w, h = A4
# print(A4)
# c = canvas.Canvas("src/reports/hello-world.pdf", pagesize=A4)
# c.drawString(50, h - 50, "Hello, world!")

# # Draw a horizontal line.
# # x = 50
# # y = h - 60
# # c.line(x, y, x + 500, y)

# text = c.beginText(50, h - 70)
# text.setFont("Times-Roman", 12)

# # The two sentences appear on two different lines.
# text.textLine("Hello world!")
# text.textLine("From ReportLab and Python!")

# c.drawText(text)

# c.drawImage("src/assets/GrumpyBearInks.png", 480, h - 100, width=70, height=70, mask=[0,2])
# c.setFillColorRGB(0.3, 0.5, 0.4, 1)
# c.drawString(495, h - 110, "GBINKS")


# c.showPage()
# c.save()