import flet as ft
from flet_route import Params, Basket
from components.side_bar_component import SideBar
from components.appbar_components import MyAppBar
from controller import teeImages, seacrchColorGarment
import flet.canvas as cv
from custom_colors.brown_palette import Palette



class DesignerPage(ft.View):
    def __init__(self, page:ft.Page, params:Params, basket:Basket):
        super().__init__(
            route="/designer",
            padding=0
        )
        self.page = page
        self.params = params
        self.basket = basket

        self.appbar = MyAppBar("Designer")

        self.bgcolor = Palette.THEME_LIGHT

        self.sidebar = SideBar(self.page)
        self.test = ft.Ref[ft.Container]()
        self.screen_gesture = ft.GestureDetector(
            on_tap=self.sidebar.close_sidebar
        )        

        # self.gd = ft.GestureDetector(
        #     mouse_cursor=ft.MouseCursor.MOVE,
        #     content=

        #     drag_interval=10,
        #     on_pan_update=self.change_loc
        # )

        self.design_area = ft.Ref[ft.Container]()
        self.palette_area = ft.Ref[ft.Container]()

        self.body_container = ft.Container(
            col=8,
            content=ft.Stack(
                expand_loose=True,
                alignment=ft.alignment.top_center,
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        opacity=0.2,
                        content=ft.Image(
                            src="src/assets/GBI-LOGO.png",
                            fit=ft.ImageFit.COVER,
                        ),
                    ),
                    ft.Container(
                        
                        ref=self.design_area,   
                    ),
                    ft.Container(
                        ref=self.palette_area,   
                    ),
                    ft.GestureDetector(
                            mouse_cursor = ft.MouseCursor.MOVE,
                            drag_interval=10,
                            on_pan_update=self.change_loc,
                            left=200,
                            top=60,
                            
                            content=ft.Container(
                                ref=self.test,
                                width=200,
                                height=300,
                                alignment=ft.alignment.center,
                                on_long_press=self.positioning,    
                            ),
                            
                    ),
                    
                    
                ]
            )
        )

        self.images = teeImages()
        self.imageList = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

        if self.visible:
            self.populateImages()

        self.designs_list = ft.Container(
            col=1,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Text("Designs", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Draggable(
                        group="color",
                        content=ft.Container(
                            content=ft.Image(
                                src="src/assets/GBI-LOGO.png",
                                width=60,
                                height=60,
                                fit=ft.ImageFit.COVER
                            ),
                        ),
                        content_feedback=ft.Image(
                            src="src/assets/GBI-LOGO.png",
                            width=20,
                            height=20,
                            fit=ft.ImageFit.COVER
                        ),
                    ),
                    
                ]
            )
        )

        self.garment_list_container = ft.Container(
            padding=ft.padding.only(0,3,0,0),
            bgcolor="white",
            col=3,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.TextField(
                        label="Search",
                        border_width=0.4,
                        border=ft.InputBorder.UNDERLINE,
                        helper_text="Type garment color",
                        helper_style=ft.TextStyle(
                            size=9
                        ),
                        on_change=self.search
                    ),
                    ft.Container(
                        padding=5,
                        expand=True,
                        content=self.imageList
                    )
                    
                ]
            )
        ) 

        self.designer_controls = ft.Container(
            ft.ResponsiveRow(
                controls=[
                    self.body_container,
                    self.designs_list,
                    self.garment_list_container
                ]
            )
        )

        self.controls=[
            self.appbar,
            ft.Stack(
                expand=True,
                controls=[
                    self.designer_controls,
                    self.screen_gesture,
                    self.sidebar ,
                    
                ]
            ),
            ft.BottomAppBar(
                shadow_color="black",
                height=50,
                bgcolor=Palette.THEME_DARK,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.PopupMenuButton(
                                    icon=ft.Icons.MENU, icon_color=Palette.THEME_LIGHT,
                                    items=[
                                        ft.PopupMenuItem(text="New MockUp"),
                                        ft.PopupMenuItem(text="Save MockUp"),
                                        ft.PopupMenuItem(text="Load Design", on_click=self.add_design),
                                        ft.PopupMenuItem(text="Clear Design", on_click=self.clear_design),
                                        ft.PopupMenuItem(text="Settings"),
                                    ]
                                ),
                                ft.Slider(min=2, max=22, divisions=20, label="{value}%", on_change=self.change_size)
                            ]
                        ),
                        ft.Text("© 2025 GBI All rights reserved", size=12, color="white", text_align=ft.TextAlign.RIGHT)
                    ]
                )
            )
        ]

    def change_size(self, e):
        if self.test.current.content:
            self.test.current.content.scale = 0.1 * e.control.value # type: ignore
            # self.test.current.content.width = 2 * e.control.value
            self.test.current.update()

    def clear_design(self, e):
        self.design_area.current.content = None
        self.design_area.current.update()
        self.palette_area.current.content = None
        self.palette_area.current.update()
        self.test.current.content = None
        self.test.current.update()

    def add_design(self, e):
        print("Adding design")
        self.test.current.content = ft.Image(src="src/assets/GBI-LOGO.png")
        self.test.current.update()

    def change_loc(self, e: ft.DragUpdateEvent):
        print("Changing location")
        e.control.top = e.control.top + e.delta_y
        e.control.left = e.control.left + e.delta_x
        e.control.update()


    def positioning(self, e):
        self.test.current.top = e.local_y - 150
        self.test.current.left = e.local_x - 150
        self.test.current.update()

    def populateImages(self):
        for image in self.images:
            self.imageList.controls.append(
                ft.ListTile(
                    title=ft.Text(image[0], size=12, weight=ft.FontWeight.BOLD),
                    leading=ft.Image(src=image[1]),
                    data=image[1],
                    on_long_press=self.load_image,
                    
                )
            )

    def search(self, e):
        print(e.control.value)
        self.imageList.controls.clear()
        self.imageList.update()
        search_data = seacrchColorGarment(e.control.value)
        for image in search_data:
            self.imageList.controls.append(
                ft.ListTile(
                    title=ft.Text(image[0]),
                    leading=ft.Image(src=image[1]),
                    data=image[1],
                    on_long_press=self.load_image,
                    
                ) 
            )
        self.imageList.update()

    def load_image(self, e):
        print(f"Loading {e.control.data}")
        self.design_area.current.content = ft.Image(src=e.control.data)
        self.design_area.current.update()
        self.palette_area.current.content = ft.Text(e.control.title.value)
        self.palette_area.current.update()

    def drag_will_accept(self, e):
        e.control.content.border = ft.border.all(
            2, ft.Colors.BLACK45 if e.data == "true" else ft.Colors.RED
        )
        e.control.update()

    def drag_accept(self, e: ft.DragTargetEvent):
        src = self.page.get_control(f"{e.src_id}") # type: ignore
        # print(e.control.content)
        print(e.x)
        print(e.y)
        e.control.content.content = ImageTest(src.content.content.src) # type: ignore # ft.Image(src.content.src, height=100, width=100)
        e.control.content.border = None
        e.control.update()

    def drag_leave(self, e):
        e.control.content.border = None
        e.control.update()

class ImageTest(ft.Image):
    def __init__(self, img):
        super().__init__()

        self.src = img
        self.height=100
        self.width=100

        
        
