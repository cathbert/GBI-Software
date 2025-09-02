import flet as ft


class SideBar(ft.Stack):
    def __init__(self, page:ft.Page):
        super().__init__()
        self.THEME_DARK = "#643a1e"
        self.MID_COLOR = "#a45520"
        self.THEME_LIGHT = "#bb824d"

        self.opacity=0.7
        self.offset=ft.Offset(-0.88, 0)
        self.animate_offset=ft.Animation(400, ft.AnimationCurve.EASE_IN_OUT)
        self.animate_opacity=True
        self.animate_position=True

        self.open_close_sidebar = ft.Ref[ft.IconButton]()
        
        self.controls=[
            ft.Container(
                    border_radius=ft.border_radius.only(0,10,0,10),
                    expand=True,
                    bgcolor=self.THEME_DARK,
                    width=300,
                    height=660,
                    padding=ft.padding.only(8,35,10,0),
                    
                    content=ft.Column(
                        controls=[
                            ft.Divider(
                                color=self.THEME_LIGHT
                            ),
                            ft.Column(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.TextButton(
                                        text="Dashboard",
                                        icon=ft.Icons.DASHBOARD,
                                        icon_color=self.THEME_LIGHT,
                                        style=ft.ButtonStyle(
                                            color=self.THEME_LIGHT,
                                            elevation=5,
                                            icon_size=22,
                                            bgcolor="#251f00",
                                            overlay_color = self.MID_COLOR,
                                            shadow_color="black"
                                        ),
                                        on_click=self.goToDashbord
                                    ),
                                    ft.TextButton(
                                        text="Point of sale",
                                        icon=ft.Icons.POINT_OF_SALE,
                                        icon_color=self.THEME_LIGHT,
                                        style=ft.ButtonStyle(
                                            color=self.THEME_LIGHT,
                                            elevation=5,
                                            icon_size=22,
                                            bgcolor="#251f00",
                                            overlay_color = self.MID_COLOR,
                                            shadow_color="black"
                                        ),
                                        on_click=self.goToPointOfSale
                                    ),
                                    ft.TextButton(
                                        text="Orders",
                                        icon=ft.Icons.WALLET,
                                        icon_color=self.THEME_LIGHT,
                                        style=ft.ButtonStyle(
                                            color=self.THEME_LIGHT,
                                            elevation=5,
                                            icon_size=22,
                                            bgcolor="#251f00",
                                            overlay_color = self.MID_COLOR,
                                            shadow_color="black"
                                        ),
                                        on_click=self.goToOrders
                                    ),
                                    ft.TextButton(
                                        text="Designer",
                                        icon=ft.Icons.DESIGN_SERVICES,
                                        icon_color=self.THEME_LIGHT,
                                        style=ft.ButtonStyle(
                                            color=self.THEME_LIGHT,
                                            elevation=5,
                                            icon_size=22,
                                            bgcolor="#251f00",
                                            overlay_color = self.MID_COLOR,
                                            shadow_color="black"
                                        ),
                                        on_click=self.goToDesigner
                                    ),
                                    ft.TextButton(
                                        text="Clients",
                                        icon=ft.Icons.PEOPLE,
                                        icon_color=self.THEME_LIGHT,
                                        style=ft.ButtonStyle(
                                            color=self.THEME_LIGHT,
                                            elevation=5,
                                            icon_size=22,
                                            bgcolor="#251f00",
                                            overlay_color = self.MID_COLOR,
                                            shadow_color="black"
                                        ),
                                        on_click=self.goToClients
                                    ),
                                    ft.TextButton(
                                        text="Tools",
                                        icon=ft.Icons.GARAGE,
                                        icon_color=self.THEME_LIGHT,
                                        style=ft.ButtonStyle(
                                            color=self.THEME_LIGHT,
                                            elevation=5,
                                            icon_size=22,
                                            bgcolor="#251f00",
                                            overlay_color = self.MID_COLOR,
                                            shadow_color="black"
                                        ),
                                        on_click=self.goToTools
                                    ),
                                ]
                            ),
                                    ft.Divider(
                                        color=self.THEME_LIGHT
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.TextButton(
                                                text="Close Application",
                                                icon=ft.Icons.EXIT_TO_APP,
                                                icon_color=self.THEME_LIGHT,
                                                style=ft.ButtonStyle(
                                                    color=self.THEME_LIGHT,
                                                    elevation=5,
                                                    icon_size=22,
                                                    bgcolor="#251f00",
                                                    overlay_color = self.MID_COLOR,
                                                    shadow_color="black"
                                                ),
                                            ),
                                        ]
                                    )
                        ]
                    )
                ),
                ft.Container(
                    padding=ft.padding.only(10,0,0,0),
                    bgcolor=self.THEME_DARK,
                    border_radius=25,
                    width=340,
                    height=40,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "Menu", 
                                size=22,
                                color=self.THEME_LIGHT
                            ),
                            ft.IconButton(
                                ref=self.open_close_sidebar,
                                icon=ft.Icons.ARROW_FORWARD_IOS,
                                icon_color=self.THEME_LIGHT,
                                on_click=self.open_close_sidebar_w,
                                rotate=0,
                                animate_rotation=ft.Animation(600, curve=ft.AnimationCurve.ELASTIC_OUT)
                            )
                        ]
                    )
                ),       
            ]
        
    def open_close_sidebar_w(self, e):
        if (self.offset.x == -0.88): # type: ignore
            self.open_sidebar(e)
        else:
            self.close_sidebar(e)

    def open_sidebar(self, e):
        if self.page and hasattr(self.page, "client_storage") and self.page.client_storage:
            #sidebar = self.controls[0].controls[1]
            if self:
                self.open_close_sidebar.current.icon=ft.Icons.ARROW_BACK_IOS
                self.open_close_sidebar.current.rotate = 6.4
                self.open_close_sidebar.current.update()
                self.offset = ft.Offset(0, 0)
                self.opacity = 1
                self.update()
        if self.page and hasattr(self.page, "update") and callable(self.page.update):
            self.page.update()

    def close_sidebar(self, e):
        if self.page and hasattr(self.page, "client_storage") and self.page.client_storage:
            #sidebar = self.controls[0].controls[1]
            if self:
                self.open_close_sidebar.current.icon=ft.Icons.ARROW_FORWARD_IOS
                self.open_close_sidebar.current.rotate = 0
                self.open_close_sidebar.current.update()
                self.offset = ft.Offset(-0.88, 0)
                self.opacity = 0.7
                self.update() 

    def goToDashbord(self, e):
        self.page.go("/dashboard") # type: ignore

    def goToPointOfSale(self, e):
        self.page.go("/pointofsale") # type: ignore

    def goToDesigner(self, e):
        self.page.go("/designer") # type: ignore
        
    def goToOrders(self, e):
        self.page.go("/orders") # type: ignore

    def goToClients(self, e):
        self.page.go("/clients") # type: ignore

    def goToTools(self, e):
        self.page.go("/tools") # type: ignore
        