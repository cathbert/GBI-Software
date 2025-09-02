import flet as ft
import datetime
from flet_timer.flet_timer import Timer

class MyAppBar(ft.AppBar):
    def __init__(self, page_name):
        super().__init__()

        self.page_name = page_name

        self.THEME_DARK = "#643a1e"
        self.MID_COLOR = "#a45520"
        self.THEME_LIGHT = "#bb824d"

        self.leading=ft.Icon(ft.Icons.POINT_OF_SALE)
        self.bgcolor=self.THEME_DARK
        self.color=self.THEME_LIGHT
        self.elevation=7
        self.shadow_color="black"
        self.title=ft.ListTile(
            title=ft.Text(value="GRUMPY BEAR INKS 0.0.1 ", weight=ft.FontWeight.W_600, color=ft.Colors.ORANGE),
            subtitle=ft.Text(value="Built by MucaIT 2025®©", italic=True, color=self.THEME_LIGHT)
        )
        self.timer = Timer(name="timer", interval_s=1, callback=self.refresh)
        self.clock = ft.Ref[ft.Text]()
        if self.visible:
           self.time_file()

        self.actions=[
            ft.Container(
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.ORANGE,
                gradient = ft.LinearGradient(
                    colors=[ft.Colors.ORANGE, ft.Colors.TRANSPARENT],
                    begin=ft.alignment.bottom_center,
                    end=ft.alignment.top_center
                ),
                # padding=ft.padding.only(5,0,5,0),
                width=150,
                border_radius=ft.border_radius.only(0,0,10,10),
                content=ft.Text(ref=self.clock, color=ft.Colors.BLUE_ACCENT, value="00:00.00", font_family='digital_font', size=30),
                # margin=ft.margin.only(0.0,6,0)
            ),
            self.timer,
            ft.Text(value=self.page_name, color=ft.Colors.WHITE),
            ft.PopupMenuButton(
                icon=ft.Icons.MENU,
                items=[
                    ft.PopupMenuItem(
                        icon=ft.Icons.INFO,
                        text="About",
                    ),
                    ft.PopupMenuItem(
                        icon=ft.Icons.LOGOUT,
                        text="Exit",
                        on_click=self.Logout
                    ),
                    
                ]
            )
        ]
    def Logout(self, e):
        self.page.client_storage.remove("token") # type: ignore
        self.page.go("/login") # type: ignore

    def time_file(self):
        pass

    def refresh(self):
        self.clock.current.value = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock.current.update()
    
