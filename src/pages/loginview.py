import flet as ft
from flet_route import Params, Basket
from custom_colors.brown_palette import Palette
import time

class LoginPage(ft.View):
    def __init__(self, page:ft.Page, params:Params, basket:Basket):
        super().__init__(route="/")
        self.page = page
        self.params = params
        self.basket = basket

        self.bgcolor = Palette.THEME_DARK

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
                                                        bgcolor=Palette.THEME_DARK,
                                                        color=Palette.THEME_LIGHT,
                                                        width=100,
                                                        height=100,
                                                        visible=False
                                                    ),
                                                    ft.Icon(
                                                        ft.Icons.LOCK,
                                                        color=Palette.THEME_LIGHT,
                                                        size=40
                                                    )
                                                ]
                                            )
                                            ,  
                                            ft.TextField(
                                                ref=self.username,
                                                label='Username',
                                                label_style = ft.TextStyle(color=Palette.THEME_DARK),
                                                text_style = ft.TextStyle(color=Palette.THEME_DARK),
                                                prefix_style = ft.TextStyle(color=ft.Colors.ORANGE),
                                                fill_color=Palette.THEME_LIGHT,
                                                enable_suggestions=True,
                                                prefix_icon=ft.Icons.VERIFIED_USER,
                                                border=ft.InputBorder.UNDERLINE,
                                                filled=True
                                            ),
                                            ft.TextField(
                                                ref=self.password,
                                                label='Password',
                                                label_style = ft.TextStyle(color=Palette.THEME_DARK),
                                                text_style = ft.TextStyle(color=Palette.THEME_DARK),
                                                filled=True,
                                                fill_color=Palette.THEME_LIGHT,
                                                enable_suggestions=True,
                                                prefix_icon=ft.Icons.LOCK_PERSON,
                                                border=ft.InputBorder.UNDERLINE,
                                                password=True,
                                                can_reveal_password=True,
                                                multiline=False
                                            ),
                                            ft.ElevatedButton(
                                                icon=ft.Icons.ARROW_FORWARD_IOS,
                                                icon_color=Palette.THEME_LIGHT,
                                                color=Palette.THEME_LIGHT,
                                                bgcolor=Palette.THEME_DARK,
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
            self.page.go("/dashboard") # type: ignore
            
            self.progress.current.visible=False
            
        else:
            self.progress.current.visible=False
            self.page.update() # type: ignore
            self.username.current.value = ""
            self.password.current.value = ""
            self.username.current.error_text="Wrong username"
            self.password.current.error_text="Wrong password"


        

