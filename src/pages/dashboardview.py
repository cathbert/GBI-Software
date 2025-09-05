import flet as ft
from flet_route import Params, Basket
from components.barchartcomponents import SampleRod
from components.side_bar_component import SideBar
from components.appbar_components import MyAppBar
import matplotlib
import matplotlib.pyplot as plt
from database import Database
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import numpy as np

from flet.matplotlib_chart import MatplotlibChart

matplotlib.use("svg")

class DashboardPage(ft.View):
    def __init__(self, page:ft.Page, params:Params, basket:Basket):
        super().__init__(
            route="/dashbord",
            padding=0
        )
        self.page = page
        self.params = params
        self.basket = basket

        self.db = Database()
        self.theme = self.db.getTheme()

        self.bgcolor = self.theme[5]
        self.appbar = MyAppBar("Dashboard")

        # =========================================BAR CHART========================================
        self.chart = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=0,
                    bar_rods=[SampleRod(5)],
                ),
                ft.BarChartGroup(
                    x=1,
                    bar_rods=[SampleRod(6.5)],
                ),
                ft.BarChartGroup(
                    x=2,
                    bar_rods=[SampleRod(15)],
                ),
                ft.BarChartGroup(
                    x=3,
                    bar_rods=[SampleRod(7.5)],
                ),
                ft.BarChartGroup(
                    x=4,
                    bar_rods=[SampleRod(9)],
                ),
                ft.BarChartGroup(
                    x=5,
                    bar_rods=[SampleRod(11.5)],
                ),
                ft.BarChartGroup(
                    x=6,
                    bar_rods=[SampleRod(6)],
                ),
                ft.BarChartGroup(
                    x=7,
                    bar_rods=[SampleRod(6)],
                ),
                ft.BarChartGroup(
                    x=8,
                    bar_rods=[SampleRod(6)],
                ),
                ft.BarChartGroup(
                    x=9,
                    bar_rods=[SampleRod(6)],
                ),
                ft.BarChartGroup(
                    x=10,
                    bar_rods=[SampleRod(6)],
                ),
                ft.BarChartGroup(
                    x=11,
                    bar_rods=[SampleRod(6)],
                ),
            ],
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=0, label=ft.Text("JAN")),
                    ft.ChartAxisLabel(value=1, label=ft.Text("FEB")),
                    ft.ChartAxisLabel(value=2, label=ft.Text("MAR")),
                    ft.ChartAxisLabel(value=3, label=ft.Text("APR")),
                    ft.ChartAxisLabel(value=4, label=ft.Text("MAY")),
                    ft.ChartAxisLabel(value=5, label=ft.Text("JUN")),
                    ft.ChartAxisLabel(value=6, label=ft.Text("JUL")),
                    ft.ChartAxisLabel(value=7, label=ft.Text("AUG")),
                    ft.ChartAxisLabel(value=8, label=ft.Text("SEP")),
                    ft.ChartAxisLabel(value=9, label=ft.Text("OCT")),
                    ft.ChartAxisLabel(value=10, label=ft.Text("NOV")),
                    ft.ChartAxisLabel(value=11, label=ft.Text("DEC")),
                ],
            ),
            on_chart_event=self.on_chart_event,
            interactive=True,
        )

        # =========================================END BAR CHART========================================
        
        # =========================================MATPLOT BAR CHART=====================================
        self.fig, self.ax = plt.subplots()

        self.fruits = ["Tees", "Hoodies", "Train Trunks", "Vests"]
        self.counts = [40, 100, 30, 55]
        self.bar_labels = ["red", "blue", "_red", "orange"]
        self.bar_colors = ["tab:red", "tab:blue", "tab:red", "tab:orange"]
        self.fig.tight_layout(pad=3.0, w_pad=2.)
        self.ax.bar(self.fruits, self.counts, label=self.bar_labels, color=self.bar_colors)
        self.ax.set_ylabel("Products")
        self.ax.set_title("Jobs")
        self.ax.legend(title="Products Colors")
        # =========================================END MATPLOT BAR CHART ==================================

        self.open_close_sidebar = ft.Ref[ft.IconButton]()
        self.sidebar = SideBar(self.page)
        self.screen_gesture = ft.GestureDetector(
            on_tap=self.sidebar.close_sidebar
        )

        # =======================================MAT LINE===================================
        # Fixing random state for reproducibility
        np.random.seed(19680801)

        dt = 0.01
        t = np.arange(0, 30, dt)
        nse1 = np.random.randn(len(t))  # white noise 1
        nse2 = np.random.randn(len(t))  # white noise 2

        # Two signals with a coherent part at 10Hz and a random part
        s1 = np.sin(2 * np.pi * 10 * t) + nse1
        s2 = np.sin(2 * np.pi * 10 * t) + nse2

        mfig, axs = plt.subplots(2, 1)
        axs[0].plot(t, s1, t, s2)
        axs[0].set_xlim(0, 2)
        axs[0].set_xlabel("time")
        axs[0].set_ylabel("s1 and s2")
        axs[0].grid(True)

        cxy, f = axs[1].cohere(s1, s2, 256, 1.0 / dt)
        axs[1].set_ylabel("coherence")

        mfig.tight_layout()
        # ==================================================================================

        self.dashboard_controls = ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                col=6,
                                expand=True,
                                bgcolor=self.theme[1],
                                content=self.chart, 
                                # , padding=10, border_radius=5, expand=True
                            ), 
                            ft.Container(
                                bgcolor=self.theme[1],
                                expand=True,
                                col=6,
                                height=300,
                                
                                content=MatplotlibChart(
                                    figure=self.fig, 
                                    expand=True,
                                    transparent=True
                                )
                            )
                            
                        ]
                    ),
                    ft.Tabs(
                        selected_index=0,
                        indicator_color=self.theme[3],
                        divider_color=self.theme[6],
                        label_color=self.theme[2],
                        overlay_color=self.theme[6],
                        tabs=[
                             ft.Tab(
                                  text="Overall Sales",
                                  content=ft.Container(
                                       col=12,
                                       content=MatplotlibChart(mfig, expand=True)
                                  )
                             ),
                             ft.Tab(
                                  text="Text"
                             ),
                             ft.Tab(
                                  text="Text"
                             )
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
                    self.dashboard_controls,
                    # self.screen_gesture,
                    self.sidebar ,
                    
                ]
            )
        ]

    def on_chart_event(self, e: ft.BarChartEvent):
            for group_index, group in enumerate(self.chart.bar_groups):
                for rod_index, rod in enumerate(group.bar_rods):
                    rod.hovered = e.group_index == group_index and e.rod_index == rod_index
            self.chart.update()

    