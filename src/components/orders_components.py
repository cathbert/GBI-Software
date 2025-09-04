import flet as ft
from database import Database
import os

class MyDataRow(ft.DataRow):
    def __init__(self, id, order_number, description, date, client, completed):
        self.id = id
        self.order_number = order_number
        self.description = description
        self.date = date
        self.client = client
        self.completed = completed

        self.deletion_alert = ft.Ref[ft.AlertDialog]()
        self.change_status_alert = ft.Ref[ft.AlertDialog]()

        self.db = Database()
        self.theme = self.db.getTheme()

        super().__init__(
            cells = [
            ft.DataCell(content=ft.Text(value=self.id, color=self.theme[8])),
            ft.DataCell(ft.Text(self.order_number, color=self.theme[8])),
            ft.DataCell(ft.Text(self.description, color=self.theme[8])),
            ft.DataCell(ft.Text(str(self.date), color=self.theme[8])),
            ft.DataCell(ft.Text(self.client, color=self.theme[8])),
            ft.DataCell(ft.IconButton(ft.Icons.CHECK, icon_color="#9bff65", on_click=self.change_order_status) if self.completed else ft.IconButton(ft.Icons.CANCEL, icon_color="#ff2e2e", on_click=self.change_order_status)),
        ]
        )

        self.on_long_press = self.data_prev

    def change_order_status(self, e):
        self.page.open(ft.AlertDialog( # type: ignore
            ref=self.change_status_alert,
            title=ft.Text("Do you wish to change Order status?", font_family="reddit-bold"),
            content=ft.Row(
                controls=[
                    ft.Switch(label="Current Status", value=self.cells[0].content.value), # type: ignore
                    ft.TextField(label="Password")
                ]
            ),
            actions=[
                ft.ElevatedButton("Change Order Status", on_click=self.change, bgcolor=self.theme[6], color=self.theme[0])
            ]
        ))
        self.update()

    def change(self, e):
        if self.db.updateOrderStatus(self.id, e.control.parent.content.controls[0].value):
            e.control.parent.open = False
            e.control.parent.update()
            self.parent.parent.update() # type: ignore
            self.cells[0].content.update()


    def data_prev(self,e):
        self.page.open(ft.AlertDialog( # type: ignore
            ref=self.deletion_alert,
            title=ft.Text("Do you wish to delete Order?"),
            actions_alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            actions=[
                ft.ElevatedButton("Delete Order", on_click=self.order_deletion),
                ft.ElevatedButton("Cancel Deletion")
            ]
        ))
        # order_number = self.cells[0].content.value # type: ignore
        # description = self.cells[1].content.value # type: ignore
        # date = self.cells[2].content.value # type: ignore
        # client = self.cells[3].content.value # type: ignore
        # completed = self.cells[4].content.value # type: ignore

    def order_deletion(self, e):
        if self.db.deleteOrder(self.id):
            e.control.parent.open=False
            e.control.parent.update()
            # self.parent.update() # type: ignore
            os.remove(f"src/reports/{self.order_number}.pdf")
            self.parent.parent.update() # type: ignore

        

        


         
        