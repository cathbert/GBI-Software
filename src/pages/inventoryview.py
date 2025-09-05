import flet as ft
from flet_route import Params, Basket
from components.side_bar_component import SideBar
from components.appbar_components import MyAppBar
from database import Database


class InventoryPage(ft.View):
    def __init__(self, page:ft.Page, params:Params, basket:Basket):
        super().__init__(
            route="/inventory",
            padding=0
        )
        self.page = page
        self.params = params
        self.basket = basket

        self.db = Database()
        self.theme = self.db.getTheme()

        self.appbar = MyAppBar("Inventory")

        self.bgcolor = self.theme[2]

        self.sidebar = SideBar(self.page)

        self.garments_page = ft.Container(
            expand=True,
            bgcolor=self.theme[2],
            col=12,
            content=ft.Column(
                controls=[
                    ft.Container(
                        border_radius=ft.border_radius.only(10,0,0,10),
                        bgcolor=self.theme[6],
                        padding=ft.padding.only(10,0,0,0),
                        margin=ft.margin.only(100,0,0,0),
                        content=ft.Row(
                            controls=[
                                ft.Text("Garments", size=20)
                            ]
                        )
                    )
                ]
            )
        )
        self.inks_page = ft.Container(
            content=ft.Text("Inks")
        )
        self.tools_page = ft.Container(
            content=ft.Text("Tools")
        )

        self.body = ft.Container(
            col=10,
            bgcolor=self.theme[5],
            border_radius=10
        )
        self.rightbar = ft.Container(
            col=2,
            bgcolor=self.theme[5],
            border_radius=10,
            content=ft.Column(
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.Dropdown(
                            on_change=self.callPage,
                            border=None,
                            expand=True,
                            options=[
                                ft.DropdownOption(
                                    key="Garments"
                                ),
                                ft.DropdownOption(
                                    key="Inks"
                                ),
                                ft.DropdownOption(
                                    key="Tools"
                                ),
                                ft.DropdownOption(
                                    key=""
                                )
                            ],
                            label="Products",
                            label_style=ft.TextStyle(color=self.theme[2])
                        )
                    )
                ]
            )
        )

        self.inventory_controls = ft.Container(
            padding=2,
            content=ft.ResponsiveRow(
                spacing=2,
                controls=[
                    self.body,
                    self.rightbar
                    
                ]
            )
        )

        self.controls=[
            self.appbar,
            ft.Stack(
                expand=True,
                controls=[
                    self.inventory_controls,
                    # self.screen_gesture,
                    self.sidebar ,
                    
                ]
            )
        ]

    def callPage(self, e):
        if e.control.value == "Garments":
            self.body.content = self.garments_page
            self.body.update()
        elif e.control.value == "Inks":
            self.body.content = self.inks_page
            self.body.update()
        elif e.control.value == "Tools":
            self.body.content = self.tools_page
            self.body.update()