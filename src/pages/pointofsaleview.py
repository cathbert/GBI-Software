import flet as ft
from flet_route import Params, Basket
from components.side_bar_component import SideBar
from components.appbar_components import MyAppBar
from components.product_component import Product
from controller import teeImagesFront, generate_order_number, seacrchColorGarment
from database import Database
import datetime
from receipt_generator import Report


class POSPage(ft.View):
    def __init__(self, page:ft.Page, params:Params, basket:Basket):
        super().__init__(
            route="/pointofsale",
            padding=0
        )
        self.page = page
        self.params = params
        self.basket = basket

        self.db = Database()
        self.theme = self.db.getTheme()

        self.test = ft.Ref[ft.Image]()
        self.order_list = ft.Ref[ft.ListView]()
        self.ORDER_NUMBER = ft.Ref[ft.Text]()
        self.my_grid = ft.Ref[ft.GridView]()
        self.client = ft.Ref[ft.Dropdown]()

        self.appbar = MyAppBar("Point of Sale")

        self.bgcolor = self.theme[2]

        self.sidebar = SideBar(self.page)
        self.search_field = ft.Ref[ft.TextField]()
        self.colors = ft.Ref[ft.PopupMenuItem]()

        self.screen_gesture = ft.GestureDetector(
            on_tap=self.sidebar.close_sidebar
        )

        self.job_list = ft.Ref[ft.Dropdown]()

        # self.left_bar = ft.Container(
        #     border_radius=5,
        #     col=1, 
        #     bgcolor=Palette.THEME_DARK,
        #     content=ft.NavigationRail(
        #         destinations=[
        #             ft.NavigationRailDestination(
        #                 icon=ft.Icons.PEOPLE,
        #                 label="All"
        #             ),
        #             ft.NavigationRailDestination(
        #                 icon=ft.Icons.PAYMENT,
        #                 label="PAY"
        #             )
        #         ]
        #     )
        # )
        
        self.body = ft.Container(
            expand=True,
            col=9,
            
            content=ft.Column(
                controls=[
                    ft.Container(
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=ft.Colors.BLACK,
                            offset=ft.Offset(0, 0),
                            blur_style=ft.ShadowBlurStyle.OUTER,
                        ),
                        padding=7,
                        border_radius=5,
                        bgcolor=self.theme[1],
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.FilledButton(
                                    "New Order",
                                    bgcolor=self.theme[6],
                                    on_click=self.newOrder
                                ),
                                ft.Row(
                                    controls=[
                                        ft.TextField(
                                            ref=self.search_field,
                                            label='Search',
                                            label_style=ft.TextStyle(color=self.theme[8]),
                                            border_color=self.theme[6],
                                            on_change=self.search,
                                            disabled=True
                                        ),
                                        
                                    ]
                                )
                                
                            ]
                        ) 
                    ),
                    # Products container
                    ft.Container(
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=ft.Colors.BLACK,
                            offset=ft.Offset(0, 0),
                            blur_style=ft.ShadowBlurStyle.OUTER,
                        ),
                        expand=True, 
                        border_radius=5,
                        bgcolor=self.theme[1],
                        content=ft.GridView(
                                ref = self.my_grid,
                                disabled = True,
                                opacity = 0.4,
                                controls= [
                                    ft.Container(
                                        on_click=self.retest,
                                        border_radius=5,
                                        width=70,
                                        height=80,
                                        ink=True,
                                        content=ft.Column(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            spacing=0,
                                            controls=[
                                                ft.Container(
                                                    alignment=ft.alignment.center,
                                                    content=ft.Image(
                                                        ref=self.test,
                                                        src=product[1]
                                                        # animate_scale=
                                                    ),
                                                ),
                                                ft.Container(
                                                    #opacity=0.5,
                                                    bgcolor=self.theme[0],
                                                    border_radius=ft.border_radius.only(0,0,5,5),
                                                    alignment=ft.alignment.center,
                                                    margin=ft.margin.only(0,-30,0,0),
                                                    content=ft.Container(
                                                        content=ft.Text(product[0]),
                                                    ),
                                                    
                                                    data={"title" : product[0], "image" : product[1]}
                                                )
                                                
                                                
                                            ]
                                        )
                                    ) for product in teeImagesFront()
                                ], # [Product(title=i[0], image=i[1]) for i in teeImages() ],
                                expand=1,
                                runs_count=5,
                                max_extent=200,
                                child_aspect_ratio=0.8,
                                spacing=5,
                                run_spacing=5
                        )
                    ) 
                ]
            )
        )

        self.progress = ft.AlertDialog(
            bgcolor=ft.Colors.TRANSPARENT,
            
            content=ft.ProgressRing(
                expand=True,
                width=200,
                height=200,
                color=self.theme[1]
            )
        )

        self.right_bar = ft.Container(
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.BLACK,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.INNER,
            ),
            col=3, 
            expand=True, 
            border_radius=5,
            bgcolor=self.theme[1], 
            content=ft.Column(
                spacing=1,
                controls=[
                    ft.Container(
                        padding=5,
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.RECEIPT, color=self.theme[6]),
                                ft.Text(
                                    value="INVOICE: ",
                                    weight=ft.FontWeight.BOLD,
                                    color="white"
                                ),
                                ft.Text(
                                    ref = self.ORDER_NUMBER,
                                    weight=ft.FontWeight.BOLD
                                )
                            ]
                        )
                    ),
                    ft.Divider(
                        color=self.theme[2]
                    ),
                    ft.Container(
                        content=ft.Dropdown(
                            ref=self.client,
                            expand=True,
                            editable=True,
                            enable_filter=True,
                            label="Client",
                            filled=True,
                            disabled=True,
                            border=ft.InputBorder.UNDERLINE,
                            on_change=self.grifter,
                            options=[
                                ft.DropdownOption(
                                    key=client[0],
                                    text = f"{client[1]} {client[2]}",
                                    on_click=self.grifter   
                                ) for client in self.db.getClients()
                            ]
                        )
                    ),
                    ft.Container(
                        expand=True,
                        margin=3,
                        bgcolor=self.theme[2],
                        height=500,
                        content=ft.ListView(
                            ref=self.order_list,
                        )
                    ),
                    ft.Container(
                        margin=ft.margin.only(5,0,5,0),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text('TOTAL', size=20, color=self.theme[8]),
                                ft.Text('300.00', size=20, weight=ft.FontWeight.BOLD),
                            ]
                        ),
                    ),
                    ft.Container(
                        margin=5,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            controls=[
                                ft.ElevatedButton(
                                    text="Create Order",
                                    color=self.theme[0],
                                    bgcolor=self.theme[8],
                                    on_click=self.create_order
                                    # style=ft.ButtonStyle(
                                    #     color=ft.Colors.ORANGE,
                                    #     bgcolor=ft.Colors.ORANGE
                                    # )
                                ),
                                ft.ElevatedButton(
                                    text="Cancel Order",
                                    color=ft.Colors.RED,
                                    bgcolor=self.theme[8],
                                    on_click=self.cancelOrder
                                    # style=ft.ButtonStyle(
                                    #     color=ft.Colors.ORANGE,
                                    #     bgcolor=ft.Colors.ORANGE
                                    # )
                                )
                            ]
                        )
                    )
                    
                ]
            )
        )
        self.my_progress_stack = ft.Ref[ft.Stack]()
        self.point_of_sale_controls = ft.Container(
            padding=5,
            expand=True,
            content=ft.Stack(
                expand=True,
                ref=self.my_progress_stack,
                controls=[
                    ft.ResponsiveRow(
                        expand=True,
                        controls=[
                            # self.left_bar,
                            self.body,
                            self.right_bar
                        ]
                    )
                ]
            )
        )
        
        

        self.controls=[
            self.appbar,
            ft.Stack(
                expand=True,
                controls=[
                    self.point_of_sale_controls,
                    # self.screen_gesture,
                    self.sidebar ,   
                ]
            )
        ]

    def grifter(self, e):
        # print(e.control)
        pass

    def create_order(self, e):
        if self.client.current.value == None:
            self.page.open( # type: ignore
                ft.SnackBar(
                    duration=2000,
                    content=ft.Row(
                        controls=[
                            ft.Text("😞", size=30, color="green"),
                            ft.Text("Please Add client to proceed with Order", color=ft.Colors.RED)
                        ]
                    )
                )
            )
        else:
            current_order = self.order_list.current.controls
            if len(current_order) < 1:
                self.page.open( # type: ignore
                    ft.SnackBar(
                        content=ft.Row(
                            controls=[
                                ft.Text("😞", size=30, color="green"),
                                ft.Text("You need to provide an item to create an order", color=ft.Colors.RED)
                            ]
                        )
                    )
                )
            else:
                self.page.open( # type: ignore
                    self.progress
                )
                try:
                    client = self.db.getClientById(int(self.client.current.value))
                except ValueError:
                    self.cancelOrder
                    self.page.close(self.progress)  # type: ignore
                    self.page.open( # type: ignore
                        ft.SnackBar(
                            content=ft.Row(
                                controls=[
                                    ft.Text("😞", size=30, color="green"),
                                    ft.Text("Failed to create order, please try again", color=ft.Colors.RED)
                                ]
                            )
                        )
                    )

                self.db.createOrder(order_code=self.ORDER_NUMBER.current.value, description="", date=datetime.datetime.now(), client=self.client.current.value)
                order = self.db.getOrderByCode(self.ORDER_NUMBER.current.value)
                for item in current_order:
                    self.db.createOrderItem(item=item.title.value, order_id=order[0], qty=item.subtitle.controls[2].value, colors=item.subtitle.controls[3].controls[1].value) # type: ignore
                
                report = Report(
                    self.ORDER_NUMBER.current.value, 
                    client_name=f"{client[1]} {client[2]}",
                    client_contact=f"{client[4]}",
                    client_email=f"{client[3]}",
                    client_address=f"{client[5]}",
                    order_date=order[3],
                    items=[(item.title.value,item.subtitle.controls[2].value,item.subtitle.controls[3].controls[1].value) for item in current_order]
                )
                self.ORDER_NUMBER.current.value = ""
                self.ORDER_NUMBER.current.update()
                self.order_list.current.controls.clear()
                self.order_list.current.update()
                self.my_grid.current.disabled = True
                self.my_grid.current.opacity = 0.4
                self.my_grid.current.update()
                self.client.current.value= ""
                self.client.current.disabled = True
                self.client.current.update()
                self.search_field.current.disabled = True
                self.search_field.current.update()
                self.page.close(self.progress)  # type: ignore
                self.page.open( # type: ignore
                    ft.SnackBar(
                        content=ft.Row(
                            controls=[
                                ft.Text("😎", size=30, color="green"),
                                ft.Text(f"Order: {self.ORDER_NUMBER.current.value} created!!", color=ft.Colors.LIME)
                            ]
                        )
                    )
                )
                

    def cancelOrder(self, e):
        self.my_grid.current.disabled = True
        self.my_grid.current.opacity = 0.4
        self.my_grid.current.update()
        self.order_list.current.controls.clear()
        self.order_list.current.update()
        self.client.current.disabled = True
        self.client.current.update()
        self.search_field.current.disabled = True
        self.search_field.current.update()
        

    def newOrder(self, e):
        self.ORDER_NUMBER.current.value = ""
        self.ORDER_NUMBER.current.update()
        self.ORDER_NUMBER.current.value = generate_order_number()
        self.ORDER_NUMBER.current.update()
        self.order_list.current.controls.clear()
        self.order_list.current.update()
        self.my_grid.current.disabled = False
        self.my_grid.current.opacity = 1
        self.my_grid.current.update()
        self.client.current.disabled = False
        self.client.current.update()
        self.search_field.current.disabled = False
        self.search_field.current.update()
        self.page.update() # type: ignore


    def clean_field_w(self, e):
        pass
        # print("hfjdhgkdfh")
        # self.search_field.current.value = ""
        # self.search_field.current.update()

    def search(self, e):
        print(e.control.value)
        self.my_grid.current.controls.clear()
        self.my_grid.current.update()
        for product in seacrchColorGarment(e.control.value):
            self.my_grid.current.controls.append(
                ft.Container(
                on_click=self.retest,
                border_radius=5,
                width=70,
                height=80,
                ink=True,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                    controls=[
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=ft.Image(
                                ref=self.test,
                                src=product[1]
                                # animate_scale=
                            ),
                        ),
                        ft.Container(
                            #opacity=0.5,
                            bgcolor=self.theme[0],
                            border_radius=ft.border_radius.only(0,0,5,5),
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(0,-30,0,0),
                            content=ft.Container(
                                content=ft.Text(product[0]),
                            ),
                            
                            data={"title" : product[0], "image" : product[1]}
                        )
                        
                        
                    ]
                )
            )
            )
            # self.my_grid.current.update()
        self.my_grid.current.update()
        # self.search_field.current.update()

    def retest(self, e):
        # print(e.control.content.controls[1].data)
        current = self.order_list.current.controls
        # print([i.title.value for i in current])

        if e.control.content.controls[1].data['title'] in [i.title.value for i in current]: # type: ignore
            index = [i.title.value for i in current].index(e.control.content.controls[1].data['title']) # type: ignore
            # print(current[index].title)
            current_quantity = int(current[index].subtitle.controls[2].value) # type: ignore
            current[index].subtitle.controls[2].value = str(current_quantity + 1) # type: ignore
            self.order_list.current.update()
        else:
            self.order_list.current.controls.append(
                ft.ListTile(
                    leading=ft.Image(src=e.control.content.controls[1].data['image']),
                    title=ft.Text(e.control.content.controls[1].data['title'], size=12),
                    subtitle=ft.Row(
                        controls=[
                            ft.IconButton(ft.Icons.REMOVE, on_click=self.reduce_qty, on_long_press=self.delete_item),
                            ft.Text("Qty:", size=10, italic=True), 
                            ft.Text("1", size=10, weight=ft.FontWeight.BOLD),
                            ft.Row(
                                controls=[
                                    ft.Text(value="Colors:",size=10, weight=ft.FontWeight.BOLD),
                                    ft.Text(value="0",size=10, weight=ft.FontWeight.BOLD)
                                ]
                            )
                        ]
                    ),
                    trailing=ft.PopupMenuButton(
                        popup_animation_style=ft.AnimationStyle(200, curve=ft.AnimationCurve.EASE_IN_EXPO),
                        icon=ft.Icons.MENU, 
                        icon_color=self.theme[0],
                        items=[
                            ft.PopupMenuItem(
                                ref = self.colors,
                                text="One color print",
                                on_click=self.getColors,
                                data = 1
                            ),
                            ft.PopupMenuItem(
                                text="Two color print",
                                on_click=self.getColors,
                                data = 2
                            ),
                            ft.PopupMenuItem(
                                text="Three color print",
                                on_click=self.getColors,
                                data = 3
                            ),
                            ft.PopupMenuItem(
                                text="Four color print",
                                on_click=self.getColors,
                                data = 4
                            ),
                            ft.PopupMenuItem(
                                text="Five color print",
                                on_click=self.getColors,
                                data = 5
                            ),
                            ft.PopupMenuItem(
                                text="Six color print",
                                on_click=self.getColors,
                                data = 6
                            ),
                        ]
                    ),
                ),
            )
            self.order_list.current.update()

    def delete_item(self, e):
        tile = e.control.parent.parent
        tile.parent.controls.pop(tile.parent.controls.index(tile))
        e.control.parent.update()
        # print(e.control.parent.parent.parent.controls.index(tile))
        tile.visible=False
        tile.update()
        
    def reduce_qty(self, e):
        current_value = int(e.control.parent.controls[2].value)
        tile = e.control.parent.parent
        if current_value == 1:
            e.control.parent.parent.parent.controls.pop(e.control.parent.parent.parent.controls.index(tile))
            e.control.parent.update()
        # print(e.control.parent.parent.parent.controls.index(tile))
            tile.visible=False
            tile.update()
        e.control.parent.controls[2].value = str(current_value - 1)
        e.control.parent.update()

    def getColors(self, e):
        e.control.parent.parent.subtitle.controls[3].controls[1].value = str(e.control.data)
        e.control.parent.parent.subtitle.update()
        



    