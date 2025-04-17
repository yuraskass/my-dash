import dash
import dash_html_components as html
from dash_bootstrap_components import dbc

def get_layout():
    return dbc.Container(
        [
            html.H1("Мультистраничное приложение на Dash"),
            html.Hr(),
            # Здесь будет контент страниц
            html.Div(id="page-content"),
            html.Hr(),
            dbc.NavbarSimple(
                brand="Навигация",
                brand_href="#",
                color="primary",
                dark=True,
                nav=[dbc.NavLink("Страница 1", href="/page1", id="page1-link"),
                     dbc.NavLink("Страница 2", href="/page2", id="page2-link"),
                     dbc.NavLink("Страница 3", href="/page3", id="page3-link")],
            ),
        ],
        fluid=True,
        className="p-5",
    )