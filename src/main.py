import flet as ft
from flet_route import path, Routing
from pages.loginview import LoginPage
from pages.dashboardview import DashboardPage
from pages.pointofsaleview import POSPage
from pages.designerview import DesignerPage
from pages.ordersview import OrdersPage
from pages.clientsview import ClientPage
from pages.toolsview import ToolPage
from database import Database

db = Database()
theme = db.getTheme()

def main(page: ft.Page):
    
    page.theme_mode="light" # type: ignore
    page.fonts={
        "digital_font": "src/assets/fonts/DS-DIGIT.TTF",
        "reddit-light": "src/assets/fonts/RedditSans-Light.ttf",
        "reddit-bold": "src/assets/fonts/RedditSans-Bold.ttf"
    }

    page.theme = ft.Theme(font_family="reddit-light",
                          elevated_button_theme=ft.ElevatedButtonTheme(bgcolor=theme[7]))

    define_routes = [
        path(url="/login",view=LoginPage, clear=True),
        path(url="/dashboard",view=DashboardPage, clear=True),
        path(url="/pointofsale",view=POSPage, clear=True),
        path(url="/orders",view=OrdersPage, clear=True),
        path(url="/designer",view=DesignerPage, clear=True),
        path(url="/clients",view=ClientPage, clear=True),
        path(url="/tools",view=ToolPage, clear=True)
    ]

    Routing(page=page, app_routes=define_routes)

    # =========================END ROUTES SECTION =============================================>
 
    if page.client_storage.get("token"):
        page.go("/clients")
    else:
        page.go("/login")

    
    # page.overlay.append(ft.Image(src="src/assets/MucaitLogo.png", fit=ft.ImageFit.CONTAIN, height=40, bottom=300))
    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")