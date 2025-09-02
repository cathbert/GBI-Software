import flet as ft

MID_COLOR = "#85502d"
class SampleRod(ft.BarChartRod):
    def __init__(self, y: float, hovered: bool = False):
        super().__init__()
        self.hovered = hovered
        self.y = y
        # self.tooltip = f"{self.y}"
        self.width = 18
        self.color = ft.Colors.WHITE
        self.bg_to_y = 20
        self.bg_color = ft.Colors.GREEN_300

    def before_update(self):
        self.to_y = self.y + 0.5 if self.hovered else self.y
        self.color = ft.Colors.YELLOW if self.hovered else ft.Colors.WHITE
        self.border_side = (
            ft.BorderSide(width=1, color=ft.Colors.GREEN_400)
            if self.hovered
            else ft.BorderSide(width=0, color=ft.Colors.WHITE)
        )
        super().before_update()

