import flet as ft
from custom_colors.brown_palette import Palette

class Product(ft.Container):
    def __init__(self, title, image):
        super().__init__()
        self.title=title
        self.myimage = image

        self.width=70
        self.height=80
        
        self.on_click=self.color_bg
        self.ink=True

        self.on_long_press=self.retest

        self.border_radius=5
        self.test = ft.Ref[ft.Image]()
        self.content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Image(
                        ref=self.test,
                        src=self.myimage
                        # animate_scale=
                    ),
                ),
                ft.Container(
                    #opacity=0.5,
                    bgcolor=Palette.THEME_DARK,
                    border_radius=ft.border_radius.only(0,0,5,5),
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(0,-30,0,0),
                    content=ft.Container(
                        content=ft.Text(self.title),
                    ),
                    data={"title" : self.title, "image" : self.myimage}
                )
                
                
            ]
        )

    def color_bg(self, e):
        pass

    def retest(self, e):
        print(e.control.content.controls[1].data)