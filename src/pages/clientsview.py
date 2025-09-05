import flet as ft
from flet_route import Params, Basket
from components.side_bar_component import SideBar
from components.appbar_components import MyAppBar
from database import Database
from components.clients_components import MyClientDataRow
from controller import verifyPhoneNumber, validateEmail, generateEmail



class ClientPage(ft.View):
    def __init__(self, page:ft.Page, params:Params, basket:Basket):
        super().__init__(
            route="/clients",
            padding=0
        )
        self.page = page
        self.params = params
        self.basket = basket

        self.db = Database()
        self.theme = self.db.getTheme()

        self.appbar = MyAppBar("Clients")

        self.bgcolor = self.theme[2]

        self.sidebar = SideBar(self.page)
        self.datatable = ft.Ref[ft.DataTable]()
        self.order_number = ft.Ref[ft.Text]()

        self.firstname = ft.Ref[ft.TextField]()
        self.lastname = ft.Ref[ft.TextField]()
        self.phone = ft.Ref[ft.TextField]()
        self.email = ft.Ref[ft.TextField]()
        self.address = ft.Ref[ft.TextField]()

        # self.screen_gesture = ft.GestureDetector(
        #     on_tap=self.sidebar.close_sidebar
        # ) 

        self.body = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        
                        margin=ft.margin.only(40,10,0,0),
                        content=ft.Row(
                            controls=[
                                ft.OutlinedButton(
                                    icon_color=self.theme[8],
                                    icon=ft.Icons.PERSON,
                                    text="New Client", 
                                    on_click=self.form,
                                    style=ft.ButtonStyle(
                                        color=self.theme[8],
                                        overlay_color=self.theme[6]
                                    )
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        expand=True,
                        content=ft.ListView(
                            expand=True,
                            controls=[
                               ft.DataTable(
                                    bgcolor=self.theme[3],
                                    heading_row_color=self.theme[6],
                                    ref=self.datatable,
                                    columns=[
                                        ft.DataColumn(ft.Text(font_family="reddit-bold",value="ID"), numeric=True),
                                        ft.DataColumn(ft.Text(font_family="reddit-bold",value="First name")),
                                        ft.DataColumn(ft.Text(font_family="reddit-bold",value="Last name")),
                                        ft.DataColumn(ft.Text(font_family="reddit-bold",value="Phone")),
                                        ft.DataColumn(ft.Text(font_family="reddit-bold",value="Email")), 
                                        ft.DataColumn(ft.Text(font_family="reddit-bold",value="Address")),
                                    ],
                                    rows=[
                                        MyClientDataRow(
                                            id=client[0],
                                            firstname=client[1],
                                            lastname=client[2],
                                            phone=client[4],
                                            email=client[3],
                                            address=client[5]
                                        ) for client in self.db.getClients()
                                    ],
                                ),
                            ]
                        ),
                        
                    )
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

    def form(self, e):
        self.page.open( # type: ignore
            ft.AlertDialog(
                alignment=ft.alignment.top_center,
                bgcolor=self.theme[5],
                title=ft.Row(
                    controls=[
                        ft.Text(f"NEW CLIENT", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(value="🥳", size=20)
                    ]
                ),
                content=ft.Container(
                    bgcolor=self.theme[5],
                    width=700,
                    expand=True,
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Divider(
                                thickness=.5,
                                color=self.theme[8]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                expand=True,
                                spacing=1,
                                controls=[
                                    ft.TextField(
                                        ref=self.firstname,
                                        label="First Name",
                                        multiline=True,
                                        max_lines=4,
                                        border=ft.InputBorder.NONE,
                                        filled=True,
                                        helper_text="Required!", 
                                    ),
                                    ft.TextField(
                                        ref=self.lastname,
                                        label="Last Name",
                                        multiline=True,
                                        max_lines=4,
                                        border=ft.InputBorder.NONE,
                                        filled=True,
                                        helper_text="Required!",
                                    ),
                                ]
                            ),
                            ft.TextField(
                                ref=self.email,
                                label="Email",
                                value="no_email@gbinks.com",
                                color=ft.Colors.TEAL_200,
                                
                                prefix_icon=ft.Icons.EMAIL,
                                multiline=True,
                                max_lines=4,
                                border=ft.InputBorder.NONE,
                                filled=True,
                                helper_text="Email",
                                on_change=self.checkEmail
                            ),   
                            ft.TextField(
                                ref=self.phone,
                                label="Phone",
                                prefix_icon=ft.Icons.PHONE,
                                multiline=True,
                                max_lines=4,
                                border=ft.InputBorder.NONE,
                                filled=True,
                                helper_text="Required!",
                                on_change=self.checkPhoneNumber
                            ),
                            ft.TextField(
                                ref=self.address,
                                label="Address",
                                prefix_icon=ft.Icons.HOME,
                                multiline=True,
                                max_lines=4,
                                border=ft.InputBorder.NONE,
                                filled=True,
                                helper_text="Address",
                            ),  
                        ]
                    )
                ),
                actions=[
                    ft.ElevatedButton(color=self.theme[0], bgcolor=self.theme[6],text="Create", on_click=self.add_new_client),
                ]
            )
        )

    def checkPhoneNumber(self, e):
        if verifyPhoneNumber(e.control.value):
            e.control.error_text = ""
            e.control.helper_text = "Correct Number!"
            e.control.helper_style=ft.TextStyle(color=ft.Colors.GREEN)
            e.control.update()
        else:
            e.control.error_text = "Use 0776470383 format: All numbers, 10 digits!"
            e.control.update()


    def checkEmail(self, e):
        if validateEmail(e.control.value):
            e.control.error_text = ""
            e.control.helper_text = "Correct Email!"
            e.control.helper_style=ft.TextStyle(color=ft.Colors.GREEN)
            e.control.update()
        else:
            e.control.error_text = "Use user@gbinks.com format!"
            e.control.update()

    def add_new_client(self, e):
        firstname = e.control.parent.content.content.controls[1].controls[0].value
        lastname = e.control.parent.content.content.controls[1].controls[1].value
        email = e.control.parent.content.content.controls[2].value
        phone = e.control.parent.content.content.controls[3].value
        address = e.control.parent.content.content.controls[4].value

        if firstname == "" and lastname == "" and verifyPhoneNumber(phone) is False:
            self.page.open(ft.SnackBar(behavior=ft.SnackBarBehavior.FLOATING,content=ft.Row([ft.Text("🥵", size=20), ft.Text("Please fill in required info!!")]))) # type: ignore
        
        elif len(firstname) > 0 and len(lastname) > 0 and verifyPhoneNumber(phone) is True:
            if self.db.createClient(
                fname=firstname,
                lname=lastname,
                email=email,
                cell=phone,
                address=address 
            ):
                self.page.open(ft.SnackBar(behavior=ft.SnackBarBehavior.FLOATING,content=ft.Row([ft.Text("😁", size=20), ft.Text("Client created!!")]))) # type: ignore
                e.control.parent.open=False
                e.control.parent.update()
                # print(self.db.getClientByPhone(phone))
                self.datatable.current.rows.append(MyClientDataRow( # type: ignore 
                    id = self.db.getClientByPhone(phone),
                    firstname=firstname,
                    lastname=lastname,
                    phone=phone,
                    email=email,
                    address=address,
                )) # type: ignore
                self.datatable.current.update()
            else:
                print("Failed!!")