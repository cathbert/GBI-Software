from flet.matplotlib_chart import MatplotlibChart
import flet as ft
from flet_route import Params, Basket
from components.side_bar_component import SideBar
from components.appbar_components import MyAppBar
from custom_colors.brown_palette import Palette

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

        self.controls=[
            self.appbar,
            ft.Stack(
                expand=True,
                controls=[
                    self.sidebar ,
                    
                ]
            )
        ]