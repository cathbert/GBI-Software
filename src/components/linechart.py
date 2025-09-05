import flet as ft


class State:
    toggle = True


s = State()



data_1 = [
    ft.LineChartData(
        data_points=[
            ft.LineChartDataPoint(1, 1),
            ft.LineChartDataPoint(3, 1.5),
            ft.LineChartDataPoint(5, 1.4),
            ft.LineChartDataPoint(7, 3.4),
            ft.LineChartDataPoint(10, 2),
            ft.LineChartDataPoint(12, 2.2),
            ft.LineChartDataPoint(13, 1.8),
        ],
        stroke_width=8,
        color=ft.Colors.LIGHT_GREEN,
        curved=True,
        stroke_cap_round=True,
    ),
    ft.LineChartData(
        data_points=[
            ft.LineChartDataPoint(1, 1),
            ft.LineChartDataPoint(3, 2.8),
            ft.LineChartDataPoint(7, 1.2),
            ft.LineChartDataPoint(10, 2.8),
            ft.LineChartDataPoint(12, 2.6),
            ft.LineChartDataPoint(13, 3.9),
        ],
        color=ft.Colors.PINK,
        below_line_bgcolor=ft.Colors.with_opacity(0, ft.Colors.PINK),
        stroke_width=8,
        curved=True,
        stroke_cap_round=True,
    ),
    ft.LineChartData(
        data_points=[
            ft.LineChartDataPoint(1, 2.8),
            ft.LineChartDataPoint(3, 1.9),
            ft.LineChartDataPoint(6, 3),
            ft.LineChartDataPoint(10, 1.3),
            ft.LineChartDataPoint(13, 2.5),
        ],
        color=ft.Colors.CYAN,
        stroke_width=8,
        curved=True,
        stroke_cap_round=True,
    ),
]

data_2 = [
    ft.LineChartData(
        data_points=[
            ft.LineChartDataPoint(1, 1),
            ft.LineChartDataPoint(3, 4),
            ft.LineChartDataPoint(5, 1.8),
            ft.LineChartDataPoint(7, 5),
            ft.LineChartDataPoint(10, 2),
            ft.LineChartDataPoint(12, 2.2),
            ft.LineChartDataPoint(13, 1.8),
        ],
        stroke_width=4,
        color=ft.Colors.with_opacity(0.5, ft.Colors.LIGHT_GREEN),
        stroke_cap_round=True,
    ),
    ft.LineChartData(
        data_points=[
            ft.LineChartDataPoint(1, 1),
            ft.LineChartDataPoint(3, 2.8),
            ft.LineChartDataPoint(7, 1.2),
            ft.LineChartDataPoint(10, 2.8),
            ft.LineChartDataPoint(12, 2.6),
            ft.LineChartDataPoint(13, 3.9),
        ],
        color=ft.Colors.with_opacity(0.5, ft.Colors.PINK),
        below_line_bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.PINK),
        stroke_width=4,
        curved=True,
        stroke_cap_round=True,
    ),
    ft.LineChartData(
        data_points=[
            ft.LineChartDataPoint(1, 3.8),
            ft.LineChartDataPoint(3, 1.9),
            ft.LineChartDataPoint(6, 5),
            ft.LineChartDataPoint(10, 3.3),
            ft.LineChartDataPoint(13, 4.5),
        ],
        color=ft.Colors.with_opacity(0.5, ft.Colors.CYAN),
        stroke_width=4,
        stroke_cap_round=True,
    ),
]

class MyChart(ft.LineChart):
    def __init__(self):
        super().__init__()
        self.data_series=data_1,
        
        self.border=ft.Border(
            bottom=ft.BorderSide(4, ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE))
        )
        self.left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=1,
                    label=ft.Text("1m", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Text("2m", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=3,
                    label=ft.Text("3m", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=4,
                    label=ft.Text("4m", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=5,
                    label=ft.Text("5m", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=6,
                    label=ft.Text("6m", size=14, weight=ft.FontWeight.BOLD),
                ),
            ],
            labels_size=40,
        )
        self.bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Container(
                        ft.Text(
                            "SEP",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=7,
                    label=ft.Container(
                        ft.Text(
                            "OCT",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=12,
                    label=ft.Container(
                        ft.Text(
                            "DEC",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
            ],
            labels_size=32,
        )
        self.tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY)
        self.min_y=0
        self.max_y=4
        self.min_x=0
        self.max_x=14
        # animate=5000,
        self.expand=True

    def build(self):
        return super().build()

    def toggle_data(self, e):
        if s.toggle:
            self.data_series = data_2
            self.data_series[2].point = True
            self.max_y = 6
            self.interactive = False
        else:
            self.data_series = data_1
            self.max_y = 4
            self.interactive = True
        s.toggle = not s.toggle
        self.update()

    # page.add(ft.IconButton(ft.Icons.REFRESH, on_click=self.toggle_data))

# def main(page:ft.Page):

