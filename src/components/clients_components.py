import flet as ft
from custom_colors.brown_palette import Palette
from database import Database

class MyClientDataRow(ft.DataRow):
    def __init__(self, id, firstname, lastname, phone, email, address):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.email = email
        self.address = address


        super().__init__(
                cells = [
                ft.DataCell(ft.Text(self.id, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(self.firstname, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(self.lastname, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(self.phone, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(self.email, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(self.address, color=ft.Colors.BLACK)),
            ]
        )

        self.db=Database()

        self.on_long_press = self.data_prev

    def data_prev(self,e):
        id = self.cells[0].content.value # type: ignore
        firstname = self.cells[1].content.value # type: ignore
        lastname = self.cells[2].content.value # type: ignore
        phone = self.cells[3].content.value # type: ignore
        email = self.cells[4].content.value # type: ignore
        address = self.cells[5].content.value # type: ignore

        self.page.open(ft.AlertDialog( # type: ignore
            content=ft.Container(
                content=ft.Column(
                    width=200,
                controls=[
                    ft.Text(value=id),
                    ft.TextField(read_only=True, value=firstname),
                    ft.TextField(read_only=True, value=lastname),
                    ft.TextField(read_only=True, value=phone),
                    ft.TextField(read_only=True, value=email),
                    ft.TextField(read_only=True, value=address)
                ]
            ),
            ),
            actions=[
                ft.Switch(
                   value=False,
                   on_change=self.setEditMode
                ),
                ft.ElevatedButton(text="Update", on_click=self.updateClient, disabled=True),
                ft.ElevatedButton(text="Delete", on_click=self.deleteClient)
            ]
        ))

    def updateClient(self, e):
        id = e.control.parent.content.content.controls[0].value
        firstname =e.control.parent.content.content.controls[1].value
        lastname =e.control.parent.content.content.controls[2].value
        phone =e.control.parent.content.content.controls[3].value
        email =e.control.parent.content.content.controls[4].value
        address =e.control.parent.content.content.controls[5].value

        # print(id,firstname, lastname, phone, email, address)
        if self.db.editClient(id=id, fname=firstname, lname=lastname, email=email, cell=phone, address=address):
            e.control.parent.actions[0].value=False
            e.control.parent.actions[0].update()
            e.control.disabled=True
            e.control.update()
            e.control.parent.content.content.controls[1].read_only = True
            e.control.parent.content.content.controls[2].read_only = True
            e.control.parent.content.content.controls[3].read_only = True
            e.control.parent.content.content.controls[4].read_only = True
            e.control.parent.content.content.controls[5].read_only = True
            e.control.parent.content.content.update()
            self.parent.update() # type: ignore
            self.update()
        
    def setEditMode(self, e):
        print(e.control.value)
        # print(e.control.parent.controls)
        if e.control.value:
            e.control.parent.actions[1].disabled=False
            e.control.parent.actions[1].update()
            e.control.parent.content.content.controls[1].read_only = False
            e.control.parent.content.content.controls[2].read_only = False
            e.control.parent.content.content.controls[3].read_only = False
            e.control.parent.content.content.controls[4].read_only = False
            e.control.parent.content.content.controls[5].read_only = False
            e.control.parent.content.content.update()
        else:
            e.control.parent.actions[1].disabled=True
            e.control.parent.actions[1].update()
            e.control.parent.content.content.controls[1].read_only = True
            e.control.parent.content.content.controls[2].read_only = True
            e.control.parent.content.content.controls[3].read_only = True
            e.control.parent.content.content.controls[4].read_only = True
            e.control.parent.content.content.controls[5].read_only = True
            e.control.parent.content.content.update()

    def deleteClient(self, e):
        id = int(e.control.parent.content.content.controls[0].value)
        if self.db.deleteClient(id):
            e.control.parent.open = False
            e.control.parent.update()
            self.parent.update() # type: ignore
            self.page.open( # type: ignore
                ft.SnackBar(
                    content=ft.Row(
                        controls=[
                            ft.Text("🤐", size=20),
                            ft.Text("Client kicked out!", color=ft.Colors.LIME)
                        ]
                    )
                )
            )
        else:
            self.page.open( # type: ignore
                ft.SnackBar(
                    content=ft.Row(
                        controls=[
                            ft.Text("🤬", size=20),
                            ft.Text("Client not deleted!!", color=ft.Colors.RED)
                        ]
                    )
                )
            )

        
    