import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from app import app

layout = dbc.Container([
    html.H1('Главная страница'),
    html.P('Добро пожаловать на главную страницу'),
    dcc.Link('Прогноз по годам', href='/page1'),
    html.Br(),
    dcc.Link('Карта с показателями', href='/page2'),
    html.Br(),
    dcc.Link('Кластеризация', href='/page3')
])
