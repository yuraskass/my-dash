import dash
from dash import html, dcc
from dash.dependencies import Input, Output

from app import app
from apps import home, page1, page2, page3

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    elif pathname == '/page3':
        return page3.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run(debug=True)