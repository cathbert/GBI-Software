
import flet as ft
from flet_route import Params, Basket
from components.side_bar_component import SideBar
from components.appbar_components import MyAppBar
from tools.pantone import loadPantoneColors
from database import Database
from tools.pantone import searchPantoneUsingHex
from unit_convert import UnitConvert
import colorsys

class ToolPage(ft.View):
    def __init__(self, page:ft.Page, params:Params, basket:Basket):
        super().__init__(
            route="/tools",
            padding=0
        )
        self.page = page
        self.params = params
        self.basket = basket

        self.db = Database()
        self.theme = self.db.getTheme()        

        self.page.client_storage.remove("pantones")

        self.color_formats = ft.Ref[ft.Dropdown]()
        self.pantones_grid = ft.Ref[ft.Dropdown]()
        self.searchPantoneField = ft.Ref[ft.TextField]()

        self.bottomNumber = ft.Ref[ft.TextField]()
        self.topNumber = ft.Ref[ft.TextField]()

        self.topAnswerLabel = ft.Ref[ft.Text]()
        self.bottomAnswerLabel = ft.Ref[ft.Text]()
        self.mainAnswer = ft.Ref[ft.Text]()

        self.red_slider = ft.Ref[ft.Slider]()
        self.green_slider = ft.Ref[ft.Slider]()
        self.blue_slider = ft.Ref[ft.Slider]()

        self.color_display = ft.Ref[ft.Container]()
        self.hex_text = ft.Ref[ft.TextField]()

        # self.pantones = asyncio.run(self.db.getPantones())

        self.appbar = MyAppBar("Tools")

        self.bgcolor = self.theme[2]

        self.sidebar = SideBar(self.page)

        self.pantonePage = ft.Column(
                spacing=1,
                controls=[
                    ft.Container(
                        padding=ft.padding.all(10),
                        content=ft.Row(
                            controls=[
                                ft.TextField(
                                    ref=self.searchPantoneField,
                                    border_radius=ft.border_radius.only(10,0,0,10),
                                    fill_color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                                    label="Search Pantone Color", 
                                    expand=True,
                                    filled=True,
                                    bgcolor=ft.Colors.WHITE,
                                    border=ft.InputBorder.NONE,
                                    suffix_icon=ft.Icons.SEARCH,  
                                    on_change=self.searchPantone
                                ),
                                ft.Dropdown(
                                    # ref=self.color_formats,
                                    width=150,
                                    options=[
                                        ft.dropdown.Option("HEX"),
                                        ft.dropdown.Option("RGB"),
                                        ft.dropdown.Option("HSV"),
                                        ft.dropdown.Option("HSL"),
                                    ],
                                    label="Color Format",
                                    value="HEX",
                                    on_change=self.change_color_format
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        padding=ft.padding.only(left=10, top=-5, right=10, bottom=10),
                        expand=True,
                        content=ft.GridView(
                            ref=self.pantones_grid,
                            expand=1,
                            runs_count=5,
                            max_extent=200,
                            child_aspect_ratio=0.8,
                            spacing=5,
                            run_spacing=5,
                            controls=[
                                # ColorBox(
                                #     pantone=color[0], 
                                #     name=color[1], 
                                #     color_hex=color[2]
                                # ) for color in self.pantones
                            ]
                        )
                    )
                ]
            )

        self.conversionPage = ft.Column(
                spacing=1,
                controls=[
                    ft.Container(
                        padding=ft.padding.all(10),
                        content=ft.Row(
                            controls=[
                                ft.TextField(
                                    ref=self.topNumber,
                                    border_radius=ft.border_radius.only(10,0,0,10),
                                    fill_color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                                    label="From", 
                                    expand=True,
                                    filled=True,
                                    bgcolor=ft.Colors.WHITE,
                                    border=ft.InputBorder.NONE,
                                    suffix_icon=ft.Icons.SEARCH,  
                                    # on_change=self.searchPantone
                                ),
                                ft.Dropdown(
                                    # ref=self.color_formats,
                                    width=220,
                                    options=[
                                        ft.dropdown.Option("Centimeters"),
                                        ft.dropdown.Option("Inches"),
                                        ft.dropdown.Option("Yards"),
                                        ft.dropdown.Option("Feet"),
                                    ],
                                    label="Unit",
                                    value="HEX",
                                    on_change=self.topAnswer
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        padding=ft.padding.all(10),
                        content=ft.Row(
                            controls=[
                                ft.TextField(
                                    ref=self.bottomNumber,
                                    border_radius=ft.border_radius.only(10,0,0,10),
                                    fill_color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                                    label="To", 
                                    expand=True,
                                    filled=True,
                                    bgcolor=ft.Colors.WHITE,
                                    border=ft.InputBorder.NONE,
                                    suffix_icon=ft.Icons.SEARCH,  
                                    # on_change=self.searchPantone
                                ),
                                ft.Dropdown(
                                    # ref=self.color_formats,
                                    width=220,
                                    options=[
                                        ft.dropdown.Option("Centimeters"),
                                        ft.dropdown.Option("Inches"),
                                        ft.dropdown.Option("Yards"),
                                        ft.dropdown.Option("Feet"),
                                    ],
                                    label="Unit",
                                    value="HEX",
                                    on_change=self.bottomAnswer
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        col=12,
                        alignment=ft.alignment.center,
                        content=ft.ElevatedButton(
                            expand=True,
                            width=600,
                            text="Convert", 
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(
                                    size=18,
                                    letter_spacing=4,
                                ), 
                                color=self.theme[2],
                            ),
                            on_click=self.convert
                        ),
                    ),
                    ft.Container(
                        alignment=ft.alignment.center,
                        col=12,
                        expand=True,
                        content=ft.Column(
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    margin=ft.margin.only(0,-100,0,0),
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text(
                                                ref=self.topAnswerLabel,
                                                size=50
                                            ),
                                            ft.Text(
                                                value="to",
                                                size=50
                                            ),
                                            ft.Text(
                                                ref=self.bottomAnswerLabel,
                                                size=50
                                            )
                                        ]
                                    )
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            ref=self.mainAnswer,
                                            size=50,
                                            value="0"
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )

        self.colorPickerPage = ft.Column(
                spacing=1,
                controls=[
                    ft.Container(

                        padding=ft.padding.all(10),
                        content=ft.Row(
                            controls=[
                                ft.TextField(
                                    ref=self.topNumber,
                                    border_radius=ft.border_radius.only(10,0,0,10),
                                    fill_color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                                    label="Title", 
                                    expand=True,
                                    filled=True,
                                    bgcolor=ft.Colors.WHITE,
                                    border=ft.InputBorder.NONE,
                                    suffix_icon=ft.Icons.SEARCH,  
                                    value="Color Picker"
                                ),
                            ]
                        )
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Slider(ref=self.red_slider, min=0, max=255, divisions=255, label="{value}", on_change=self.update_color),
                                ft.Slider(ref=self.green_slider, min=0, max=255, divisions=255, label="{value}", on_change=self.update_color),
                                ft.Slider(ref=self.blue_slider, min=0, max=255, divisions=255, label="{value}", on_change=self.update_color),

                                ft.Container(ref=self.color_display, width=100, height=100, border_radius=5, bgcolor=ft.Colors.BLACK),
                                ft.TextField(ref=self.hex_text, label="Hex Code", read_only=True)
                            ]
                        )
                    )
                ]
            )

        self.body=ft.Container(
            col=10,
            content= self.pantonePage
        )
        self.right_bar=ft.Container(
            col=2,
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.OutlinedButton(
                        text="Pantones", 
                        height=40, 
                        width=300, 
                        on_click=self.callPage
                    ),
                    ft.OutlinedButton(
                        text="Conversion", 
                        height=40, 
                        width=300, 
                        on_click=self.callPage
                    ),
                    ft.OutlinedButton(
                        text="Color Picker", 
                        height=40, 
                        width=300, 
                        on_click=self.callPage
                    )
                ]
            )
        )

        self.controls=[
            self.appbar,
            ft.Stack(
                expand=True,
                controls=[
                    ft.ResponsiveRow(
                        controls=[
                            self.body,
                            self.right_bar,
                        ]
                    ),
                    self.sidebar,
                ]
            ), 
        ]

    def update_color(self, e):
        r = int(self.red_slider.current.value)
        g = int(self.green_slider.current.value)
        b = int(self.blue_slider.current.value)
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.color_display.current.bgcolor = f"#{r:02x}{g:02x}{b:02x}"# ft.Colors(r, g, b)
        self.hex_text.current.value = hex_color
        self.color_display.current.update()
        self.page.update()

    def change_color_format(self, e):
        print(e.control.value)
        self.searchPantoneField.current.prefix_text=e.control.value+"\t"
        self.searchPantoneField.current.update()

    def searchPantone(self, e):
        print(e.control.value)

    def callPage(self, e):
        if e.control.text == "Pantones":
            self.body.content=self.pantonePage
            self.body.update()
        elif e.control.text == "Conversion":
            self.body.content=self.conversionPage
            self.body.update()
        elif e.control.text == "Color Picker":
            self.body.content=self.colorPickerPage
            self.body.update()

    def topAnswer(self, e):
        self.topAnswerLabel.current.value = e.control.value
        self.topAnswerLabel.current.update()
    
    def bottomAnswer(self, e):
        self.bottomAnswerLabel.current.value = e.control.value
        self.bottomAnswerLabel.current.update()

    def convert(self, e):
        if self.topNumber.current.value == "":
            self.page.open(ft.AlertDialog(content=ft.Text("'From' cannot be NONE!"))) # type: ignore
        elif self.topAnswerLabel.current.value == None:
            self.page.open(ft.AlertDialog(content=ft.Text("Please select Unit"))) # type: ignore
        elif self.bottomAnswerLabel.current.value == None:
            self.page.open(ft.AlertDialog(content=ft.Text("'To' cannot be NONE!"))) # type: ignore
        # print(self.topNumber.current.value)
        top_unit_label = self.topAnswerLabel.current.value
        bottom_unit_label = self.bottomAnswerLabel.current.value
        
        # Inches to CM
        if top_unit_label == "Inches" and bottom_unit_label == "Centimeters":
            try:
                # ans = int(self.topNumber.current.value) * 2.54
                ans = UnitConvert(inches=int(self.topNumber.current.value))['centimetres'] # type: ignore
                self.mainAnswer.current.value = str(ans)+"cm"
                self.mainAnswer.current.update()
            except ValueError:
                self.page.open(ft.AlertDialog(content=ft.Text("Please alert fields"))) # type: ignore

        # CM tp Inches
        elif top_unit_label == "Centimeters" and bottom_unit_label == "Inches":
            try:
                # ans = int(self.topNumber.current.value) * 2.54
                ans = UnitConvert(centimetres=float(self.topNumber.current.value))['inches'] # type: ignore
                self.mainAnswer.current.value = str(round(ans, 2))+"inch/es"
                self.mainAnswer.current.update()
            except ValueError:
                self.page.open(ft.AlertDialog(content=ft.Text("Please alert fields"))) # type: ignore

        # CM to Yards
        elif top_unit_label == "Centimeters" and bottom_unit_label == "Yards":
            try:
                # ans = int(self.topNumber.current.value) * 2.54
                ans = UnitConvert(centimetres=float(self.topNumber.current.value))['yards'] # type: ignore
                self.mainAnswer.current.value = str(round(ans, 2))+"yd"
                self.mainAnswer.current.update()
            except ValueError:
                self.page.open(ft.AlertDialog(content=ft.Text("Please alert fields"))) # type: ignore

        # Yards to CM
        elif top_unit_label == "Yards" and bottom_unit_label == "Centimeters":
            try:
                # ans = int(self.topNumber.current.value) * 2.54
                ans = UnitConvert(yards=float(self.topNumber.current.value))['centimetres'] # type: ignore
                self.mainAnswer.current.value = str(round(ans, 2))+"cm"
                self.mainAnswer.current.update()
            except ValueError:
                self.page.open(ft.AlertDialog(content=ft.Text("Please alert fields"))) # type: ignore

        # Inches to Yards
        elif top_unit_label == "Inches" and bottom_unit_label == "Yards":
            try:
                # ans = int(self.topNumber.current.value) * 2.54
                ans = UnitConvert(inches=float(self.topNumber.current.value))['yards'] # type: ignore
                self.mainAnswer.current.value = str(round(ans, 2))+"yd"
                self.mainAnswer.current.update()
            except ValueError:
                self.page.open(ft.AlertDialog(content=ft.Text("Please alert fields"))) # type: ignore

        # Yards to Inches
        elif top_unit_label == "Yards" and bottom_unit_label == "Inches":
            try:
                # ans = int(self.topNumber.current.value) * 2.54
                ans = UnitConvert(yards=float(self.topNumber.current.value))['inches'] # type: ignore
                self.mainAnswer.current.value = str(round(ans, 2))+"i"
                self.mainAnswer.current.update()
            except ValueError:
                self.page.open(ft.AlertDialog(content=ft.Text("Please alert fields"))) # type: ignore
            
        # Feet to Inches
        elif top_unit_label == "Feet" and bottom_unit_label == "Inches":
            try:
                # ans = int(self.topNumber.current.value) * 2.54
                ans = UnitConvert(feet=float(self.topNumber.current.value))['inches'] # type: ignore
                self.mainAnswer.current.value = str(round(ans, 2))+"i"
                self.mainAnswer.current.update()
            except ValueError:
                self.page.open(ft.AlertDialog(content=ft.Text("Please alert fields"))) # type: ignore
        
        # Inches to Feet
        elif top_unit_label == "Inches" and bottom_unit_label == "Feet":
            try:
                # ans = int(self.topNumber.current.value) * 2.54
                ans = UnitConvert(inches=float(self.topNumber.current.value))['feet'] # type: ignore
                self.mainAnswer.current.value = str(round(ans, 2))+"ft"
                self.mainAnswer.current.update()
            except ValueError:
                self.page.open(ft.AlertDialog(content=ft.Text("Please alert fields"))) # type: ignore

        # Yards to Feet
        elif top_unit_label == "Yards" and bottom_unit_label == "Feet":
            try:
                # ans = int(self.topNumber.current.value) * 2.54
                ans = UnitConvert(yards=float(self.topNumber.current.value))['feet'] # type: ignore
                self.mainAnswer.current.value = str(round(ans, 2))+"ft"
                self.mainAnswer.current.update()
            except ValueError:
                self.page.open(ft.AlertDialog(content=ft.Text("Please alert fields"))) # type: ignore

        # Feet to Yards
        elif top_unit_label == "Feet" and bottom_unit_label == "Yards":
            try:
                # ans = int(self.topNumber.current.value) * 2.54
                ans = UnitConvert(feet=float(self.topNumber.current.value))['yards'] # type: ignore
                self.mainAnswer.current.value = str(round(ans, 2))+"yd"
                self.mainAnswer.current.update()
            except ValueError:
                self.page.open(ft.AlertDialog(content=ft.Text("Please alert fields"))) # type: ignore
        
        # Centimetres to Feet
        elif top_unit_label == "Centimeters" and bottom_unit_label == "Feet":
            try:
                # ans = int(self.topNumber.current.value) * 2.54
                ans = UnitConvert(centimetres=float(self.topNumber.current.value))['feet'] # type: ignore
                self.mainAnswer.current.value = str(round(ans, 2))+"ft"
                self.mainAnswer.current.update()
            except ValueError:
                self.page.open(ft.AlertDialog(content=ft.Text("Please alert fields"))) # type: ignore

        # Yards to Feet
        elif top_unit_label == "Feet" and bottom_unit_label == "Centimeters":
            try:
                # ans = int(self.topNumber.current.value) * 2.54
                ans = UnitConvert(feet=float(self.topNumber.current.value))['centimetres'] # type: ignore
                self.mainAnswer.current.value = str(round(ans, 2))+"cm"
                self.mainAnswer.current.update()
            except ValueError:
                self.page.open(ft.AlertDialog(content=ft.Text("Please alert fields"))) # type: ignore


class ColorBox(ft.Container):
    def __init__(self, pantone:str, name:str, color_hex:str):
        super().__init__(
            width=100,
            height=100,
            bgcolor="#"+color_hex,
            border_radius=8,
            alignment=ft.alignment.center,
        )
        self.pantone = pantone
        self.name = name
        self.color_hex = color_hex

        self.content=ft.Container(
            padding=5,
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
            content=ft.Column(
                height=60,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(pantone, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    ft.Text(name, color=ft.Colors.WHITE, weight=ft.FontWeight.W_300, size=10)
                ]
            )
        )