from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash
from app import app

from apps import map
from apps import home




app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
             [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/map':
        return map.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server()