
import flet as ft
from flet_route import Params, Basket
from components.side_bar_component import SideBar
from components.appbar_components import MyAppBar
from tools.pantone import loadPantoneColors
from database import Database
from tools.pantone import searchPantoneUsingHex

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

        # self.pantones = asyncio.run(self.db.getPantones())

        self.appbar = MyAppBar("Tools")

        self.bgcolor = self.theme[2]

        self.sidebar = SideBar(self.page)

        self.body=ft.Container(
            col=10,
            content=ft.Column(
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
                        
                    ),
                    ft.OutlinedButton(
                        text="Conversion", 
                        height=40, 
                        width=300, 
                        
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

    def change_color_format(self, e):
        print(e.control.value)
        self.searchPantoneField.current.prefix_text=e.control.value+"\t"
        self.searchPantoneField.current.update()

    def searchPantone(self, e):
        
        print(e.control.value)


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