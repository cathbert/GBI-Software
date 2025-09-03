
import flet as ft
from flet_route import Params, Basket
from components.side_bar_component import SideBar
from components.appbar_components import MyAppBar
from custom_colors.brown_palette import Palette
from tools.pantone import loadPantoneColors

class ToolPage(ft.View):
    def __init__(self, page:ft.Page, params:Params, basket:Basket):
        super().__init__(
            route="/tools",
            padding=0
        )
        self.page = page
        self.params = params
        self.basket = basket

        self.appbar = MyAppBar("Tools")

        self.bgcolor = Palette.THEME_LIGHT

        self.sidebar = SideBar(self.page)

        self.body=ft.Container(
            col=9,
            content=ft.GridView(
                controls=[
                    
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
                    self.sidebar ,
                    
                ]
            )
        ]

class ColorBox(ft.Container):
    def __init__(self, pantone:str, color_hex:str, name:str):
        super().__init__(
            width=100,
            height=100,
            bgcolor=color_hex,
            border_radius=8,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(pantone, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    ft.Text(name, color=ft.Colors.WHITE, weight=ft.FontWeight.W_300, size=10)
                ]
            )
        )