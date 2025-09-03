
import flet as ft
from flet_route import Params, Basket
from components.side_bar_component import SideBar
from components.appbar_components import MyAppBar
from custom_colors.brown_palette import Palette
from tools.pantone import loadPantoneColors
from database import Database
import asyncio
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
        
        # if self.page.client_storage.get("pantones") is None:
        #     self.page.client_storage.set("pantones", asyncio.run(self.db.getPantones()))

        self.page.client_storage.remove("pantones")

        self.color_formats = ft.Ref[ft.Dropdown]()
        self.pantones_grid = ft.Ref[ft.Dropdown]()

        self.appbar = MyAppBar("Tools")

        self.bgcolor = Palette.THEME_LIGHT

        self.sidebar = SideBar(self.page)

        self.body=ft.Container(
            col=9,
            content=ft.Column(
                spacing=1,
                controls=[
                    ft.Container(
                        padding=ft.padding.all(10),
                        content=ft.Row(
                            controls=[
                                ft.TextField(
                                    fill_color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                                    label="Search Pantone Color", 
                                    expand=True,
                                    filled=True, 
                                    border_radius=20,
                                    bgcolor=ft.Colors.WHITE,
                                    border=ft.InputBorder.NONE,
                                    suffix_icon=ft.Icons.SEARCH,  
                                    on_change=self.searchPantone
                                ),
                                ft.Dropdown(
                                    ref=self.color_formats,
                                    width=150,
                                    options=[
                                        ft.dropdown.Option("HEX"),
                                        ft.dropdown.Option("RGB"),
                                        ft.dropdown.Option("HSV"),
                                        ft.dropdown.Option("HSL"),
                                    ],
                                    label="Color Format",
                                    value="HEX",
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
                                ColorBox(
                                    pantone=color[0], 
                                    name=color[1], 
                                    color_hex=color[2]
                                ) for color in asyncio.run(self.db.getPantones())
                            ]
                        )
                    )
                ]
            )
        )
        self.right_bar=ft.Container(
            col=3
        )

        self.controls=[
            self.appbar,
            ft.Stack(
                expand=True,
                controls=[
                    self.body,
                    self.sidebar,
                ]
            )
        ]

    def searchPantone(self, e):
        print(self.color_formats.current.value)
        if self.color_formats.current.value == "HEX":
            e.control.prefix_text='HEX '
            # print(searchPantoneUsingHex(hex_color=e.control.value))
        elif self.color_formats.current.value == "RGB":
            e.control.prefix_text='(R,G,B) '
        elif self.color_formats.current.value == "HSV":
            e.control.prefix_text='(H,S,V) '
        elif self.color_formats.current.value == "HSL":
            e.control.prefix_text='(H,S,L) '
        e.control.update()
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