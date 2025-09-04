import flet as ft
from flet_route import Params, Basket
import time
from custom_colors.neutral_palette import Palette
from database import Database

class LoginPage(ft.View):
    def __init__(self, page:ft.Page, params:Params, basket:Basket):
        super().__init__(route="/")
        self.page = page
        self.params = params
        self.basket = basket

        self.db = Database()
       
        self.theme = self.db.getTheme()
        self.bgcolor = self.theme[6]

        self.progress = ft.Ref[ft.ProgressRing]()
        self.username = ft.Ref[ft.TextField]()
        self.password = ft.Ref[ft.TextField]()

        self.controls=[
            ft.Stack(
                expand=True,
                alignment=ft.alignment.center,
                controls=[
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center_left,
                        content=ft.Image(
                            opacity=0.5,
                            src="src/assets/GBI-LOGO.png"
                        )
                    )
                    ,
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center_right,
                        
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    width=530,
                                    height=500,
                                    padding=10,
                                    border_radius = 20,
                                    # bgcolor=self.THEME_DARK,
                                    blur=ft.Blur(16., 16., tile_mode=ft.BlurTileMode.MIRROR),
                                    content=ft.Column(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Stack(
                                                alignment=ft.alignment.center,
                                                controls=[
                                                    ft.ProgressRing(
                                                        ref=self.progress,
                                                        bgcolor=self.theme[0],
                                                        color=self.theme[7],
                                                        width=100,
                                                        height=100,
                                                        visible=False
                                                    ),
                                                    ft.Icon(
                                                        ft.Icons.LOCK,
                                                        color=self.theme[7],
                                                        size=40
                                                    )
                                                ]
                                            )
                                            ,  
                                            ft.TextField(
                                                ref=self.username,
                                                label='Username',
                                                label_style = ft.TextStyle(color=self.theme[0]),
                                                text_style = ft.TextStyle(color=self.theme[0]),
                                                prefix_style = ft.TextStyle(color=self.theme[4]),
                                                fill_color=self.theme[4],
                                                enable_suggestions=True,
                                                prefix_icon=ft.Icons.VERIFIED_USER,
                                                
                                                border=ft.InputBorder.UNDERLINE,
                                                filled=True
                                            ),
                                            ft.TextField(
                                                ref=self.password,
                                                label='Password',
                                                label_style = ft.TextStyle(color=self.theme[0]),
                                                text_style = ft.TextStyle(color=self.theme[0]),
                                                filled=True,
                                                fill_color=self.theme[4],
                                                enable_suggestions=True,
                                                prefix_icon=ft.Icons.LOCK_PERSON,
                                                border=ft.InputBorder.UNDERLINE,
                                                password=True,
                                                can_reveal_password=True,
                                                multiline=False
                                            ),
                                            ft.ElevatedButton(
                                                icon=ft.Icons.ARROW_FORWARD_IOS,
                                                icon_color=self.theme[7],
                                                color=self.theme[7],
                                                bgcolor=self.theme[0],
                                                text="Login",
                                                width=300,
                                                height=40,
                                                elevation=6,
                                                on_click=self.Login
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
            ),
            ft.Image(src="src/assets/MucaitLogo.png", fit=ft.ImageFit.CONTAIN, height=40)
            
        ]

    def Login(self, e):
        self.progress.current.visible=True
        if self.username.current.value == "test" and self.password.current.value == "test":
            self.page.client_storage.set("token", "sometoken") # type: ignore
            self.username.current.value = ""
            self.password.current.value = ""
            time.sleep(2)
            if self.db.getTheme() == None: # type: ignore
                self.db.addTheme(Palette.BLEND_100,
                                 Palette.BLEND_200,
                                 Palette.BLEND_300,
                                 Palette.BLEND_400,
                                 Palette.BLEND_500,
                                 Palette.BLEND_600,
                                 Palette.BLEND_700,
                                 Palette.BLEND_800,
                                 Palette.BLEND_900,)
            self.page.go("/dashboard") # type: ignore
            
            self.progress.current.visible=False
            
        else:
            self.progress.current.visible=False
            self.page.update() # type: ignore
            self.username.current.value = ""
            self.password.current.value = ""
            self.username.current.error_text="Wrong username"
            self.password.current.error_text="Wrong password"


        

