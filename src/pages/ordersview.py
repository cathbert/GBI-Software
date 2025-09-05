import flet as ft
from flet_route import Params, Basket
from components.side_bar_component import SideBar
from components.appbar_components import MyAppBar
from components.orders_components import MyDataRow
import datetime
from controller import generate_order_number, convertdate

from database import Database



class OrdersPage(ft.View):
    def __init__(self, page:ft.Page, params:Params, basket:Basket):
        super().__init__(
            route="/orders",
            padding=0
        )
        self.page = page
        self.params = params
        self.basket = basket

        self.db = Database()
        self.theme = self.db.getTheme()

        self.appbar = MyAppBar("Orders")

        self.bgcolor = self.theme[2]

        self.sidebar = SideBar(self.page)
        self.datatable = ft.Ref[ft.DataTable]()
        self.order_number = ft.Ref[ft.Text]()
        # self.screen_gesture = ft.GestureDetector(
        #     on_tap=self.sidebar.close_sidebar
        # ) 

        self.body = ft.Container(
                padding=5,
                col=12,
                content=ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(50,0,0,0),
                            content=ft.TextField(
                                prefix_icon=ft.Icons.SEARCH
                            ),
                        ),
                        
                        ft.Container(
                            bgcolor=self.theme[5],
                            expand=True,
                            padding=3,
                            content=ft.SafeArea(
                                # auto_scroll=True,
                                maintain_bottom_view_padding=True,
                                minimum_padding=5,
                                expand=True,
                                height=500,
                                    content=
                                        ft.ListView(
                                            expand=True,
                                            controls=[
                                                ft.DataTable(
                                                    bgcolor=self.theme[3],
                                                    heading_row_color=self.theme[5],
                                                    show_bottom_border=True,
                                                    show_checkbox_column=True,
                                                    vertical_lines=ft.BorderSide(width=1,color=self.theme[5]),
                                                    ref=self.datatable,
                                                    columns=[
                                                        ft.DataColumn(ft.Text(font_family="reddit-bold",value="ID")),
                                                        ft.DataColumn(ft.Text(font_family="reddit-bold",value="Order No.")),
                                                        ft.DataColumn(ft.Text(font_family="reddit-bold",value="Description")),
                                                        ft.DataColumn(ft.Text(font_family="reddit-bold",value="Date")),
                                                        ft.DataColumn(ft.Text(font_family="reddit-bold",value="Client")),
                                                        ft.DataColumn(ft.Text(font_family="reddit-bold",value="Completed"))
                                                    ],
                                                    rows=[
                                                        
                                                        MyDataRow(
                                                                    id=order[0],
                                                                    order_number=order[1], 
                                                                    description=order[2], 
                                                                    date=convertdate(order[3]),#.strftime("%A %d/%m/%Y - %I %S%p"), 
                                                                    client=order[4], 
                                                                    completed=order[5]
                                                        ) for order in self.db.getAllOrders()
                                                        # MyDataRow('978800041', '20x Tshirts', datetime.datetime.now().strftime("%A %d/%m/%Y - %I %S%p"), 'J Smith', False),
                                                        
                                            ],
                                        ),
                                    ]
                                )
                                    
                            )
                        ),
                        
                        
                    ]
                )
        )

        self.orders_controls = ft.Container(
            ft.ResponsiveRow(
                controls=[
                    self.body,
                    # self.right_bar
                    
                ]
            )
        )

        self.controls=[
            self.appbar,
            ft.Stack(
                expand=True,
                controls=[
                    self.orders_controls,
                    # self.screen_gesture,
                    self.sidebar ,
                    
                ]
            )
        ]
    def generate_order_number(self, e):
        self.order_number.current.value = ""
        self.order_number.current.update()
        self.order_number.current.value = generate_order_number()
        self.order_number.current.update()
        print("Test")

    def add_new_order(self, e):
        order_no = e.control.parent.title.controls[1].content.value
        description=e.control.parent.content.content.controls[1].value
        client = e.control.parent.content.content.controls[2].value
        self.datatable.current.rows.append(MyDataRow(order_no, description, datetime.datetime.now().strftime("%A %d/%m/%Y - %I %S%p"), client, False)) # type: ignore
        self.datatable.current.update()