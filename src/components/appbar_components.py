import flet as ft
import datetime
from flet_timer.flet_timer import Timer
from database import Database
from custom_colors import sapphire_splendour,beautiful_blue, golden_chandelier, neutral_palette, shovel_knight, dairy_made, walk_in_the_park

class MyAppBar(ft.AppBar):
    def __init__(self, page_name):
        super().__init__()

        self.page_name = page_name
        self.db = Database()
        self.theme = self.db.getTheme()

        self.leading=ft.Icon(ft.Icons.POINT_OF_SALE, color=self.theme[2])
        self.bgcolor=self.theme[8]
        self.color=self.theme[6]
        self.elevation=7
        self.shadow_color="black"
        self.title=ft.ListTile(
            title=ft.Text(value="GRUMPY BEAR INKS 0.0.1 ", weight=ft.FontWeight.W_600, color=ft.Colors.ORANGE),
            subtitle=ft.Text(value="Built by MucaIT 2025®©", italic=True, color=self.theme[2])
        )
        self.timer = Timer(name="timer", interval_s=1, callback=self.refresh)
        self.clock = ft.Ref[ft.Text]()
        if self.visible:
           self.time_file()

        self.actions=[
            ft.Container(
                alignment=ft.alignment.center,
                # bgcolor=ft.Colors.ORANGE,
                gradient = ft.LinearGradient(
                    colors=[self.theme[3], ft.Colors.TRANSPARENT],
                    begin=ft.alignment.bottom_center,
                    end=ft.alignment.top_center
                ),
                # padding=ft.padding.only(5,0,5,0),
                width=150,
                border_radius=ft.border_radius.only(0,0,10,10),
                content=ft.Text(ref=self.clock, color=self.theme[2], value="00:00.00", font_family='digital_font', size=30),
                # margin=ft.margin.only(0.0,6,0)
            ),
            self.timer,
            ft.Text(value=self.page_name, color=ft.Colors.WHITE),
            ft.PopupMenuButton(
                icon=ft.Icons.MENU,
                icon_color=self.theme[2],
                items=[
                    ft.PopupMenuItem(
                        icon=ft.Icons.INFO,
                        text="About",
                    ),
                    ft.PopupMenuItem(
                        icon=ft.Icons.SETTINGS,
                        text="Settings",
                        on_click=self.open_settings
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

    def open_settings(self, e):
        self.page.open( # type: ignore
            ft.AlertDialog(
                title=ft.Text("SETTINGS"),
                content=ft.Container(
                    width=700,
                    height=400,
                    content=ft.Column(
                        controls=[
                            ft.Dropdown(
                                # ref=self.color_formats,
                                width=150,
                                options=[
                                    ft.dropdown.Option(key="Beautiful Blue"),
                                    ft.dropdown.Option(key="Golden Chandelier"),
                                    ft.dropdown.Option(key="Neutral"),
                                    ft.dropdown.Option(key="Shovel Knight"),
                                    ft.dropdown.Option(key="Dairy Made"),
                                    ft.dropdown.Option(key="Walk in the park"),
                                    ft.dropdown.Option(key="Sapphire Splendour")
                                    # ft.dropdown.Option("HSL"),
                                ],
                                label="Themes",
                                value="Light",
                                on_change=self.change_theme
                            )
                        ]
                    )
                )
            )
        )
        
    def change_theme(self, e):
        if e.control.value == 'Beautiful Blue':
            self.db.deleteTheme()
            self.db.addTheme(beautiful_blue.Palette.BLEND_100,
                                beautiful_blue.Palette.BLEND_200,
                                beautiful_blue.Palette.BLEND_300,
                                beautiful_blue.Palette.BLEND_400,
                                beautiful_blue.Palette.BLEND_500,
                                beautiful_blue.Palette.BLEND_600,
                                beautiful_blue.Palette.BLEND_700,
                                beautiful_blue.Palette.BLEND_800,
                                beautiful_blue.Palette.BLEND_900)
            self.page.update() # type: ignore
        elif e.control.value == 'Golden Chandelier':
            self.db.deleteTheme()
            self.db.addTheme(golden_chandelier.Palette.BLEND_100,
                                golden_chandelier.Palette.BLEND_200,
                                golden_chandelier.Palette.BLEND_300,
                                golden_chandelier.Palette.BLEND_400,
                                golden_chandelier.Palette.BLEND_500,
                                golden_chandelier.Palette.BLEND_600,
                                golden_chandelier.Palette.BLEND_700,
                                golden_chandelier.Palette.BLEND_800,
                                golden_chandelier.Palette.BLEND_900)
            self.page.update() # type: ignore
        elif e.control.value == 'Neutral':
            self.db.deleteTheme()
            self.db.addTheme(neutral_palette.Palette.BLEND_100,
                                neutral_palette.Palette.BLEND_200,
                                neutral_palette.Palette.BLEND_300,
                                neutral_palette.Palette.BLEND_400,
                                neutral_palette.Palette.BLEND_500,
                                neutral_palette.Palette.BLEND_600,
                                neutral_palette.Palette.BLEND_700,
                                neutral_palette.Palette.BLEND_800,
                                neutral_palette.Palette.BLEND_900)
            self.page.update()  # type: ignore
        elif e.control.value == 'Shovel Knight':
            self.db.deleteTheme()
            self.db.addTheme(shovel_knight.Palette.BLEND_100,
                                shovel_knight.Palette.BLEND_200,
                                shovel_knight.Palette.BLEND_300,
                                shovel_knight.Palette.BLEND_400,
                                shovel_knight.Palette.BLEND_500,
                                shovel_knight.Palette.BLEND_600,
                                shovel_knight.Palette.BLEND_700,
                                shovel_knight.Palette.BLEND_800,
                                shovel_knight.Palette.BLEND_900)
            self.page.update()  # type: ignore
        elif e.control.value == 'Dairy Made':
            self.db.deleteTheme()
            self.db.addTheme(dairy_made.Palette.BLEND_100,
                                dairy_made.Palette.BLEND_200,
                                dairy_made.Palette.BLEND_300,
                                dairy_made.Palette.BLEND_400,
                                dairy_made.Palette.BLEND_500,
                                dairy_made.Palette.BLEND_600,
                                dairy_made.Palette.BLEND_700,
                                dairy_made.Palette.BLEND_800,
                                dairy_made.Palette.BLEND_900)
            self.page.update()  # type: ignore

        elif e.control.value == 'Walk in the park':
            self.db.deleteTheme()
            self.db.addTheme(walk_in_the_park.Palette.BLEND_100,
                                walk_in_the_park.Palette.BLEND_200,
                                walk_in_the_park.Palette.BLEND_300,
                                walk_in_the_park.Palette.BLEND_400,
                                walk_in_the_park.Palette.BLEND_500,
                                walk_in_the_park.Palette.BLEND_600,
                                walk_in_the_park.Palette.BLEND_700,
                                walk_in_the_park.Palette.BLEND_800,
                                walk_in_the_park.Palette.BLEND_900)
            self.page.update()  # type: ignore
        elif e.control.value == 'Sapphire Splendour':
            self.db.deleteTheme()
            self.db.addTheme(sapphire_splendour.Palette.BLEND_100,
                                sapphire_splendour.Palette.BLEND_200,
                                sapphire_splendour.Palette.BLEND_300,
                                sapphire_splendour.Palette.BLEND_400,
                                sapphire_splendour.Palette.BLEND_500,
                                sapphire_splendour.Palette.BLEND_600,
                                sapphire_splendour.Palette.BLEND_700,
                                sapphire_splendour.Palette.BLEND_800,
                                sapphire_splendour.Palette.BLEND_900)
            self.page.update()  # type: ignore