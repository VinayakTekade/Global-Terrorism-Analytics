from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash
import webbrowser
from threading import Timer

from app import app
from apps import map
from apps import home
from apps import chart
from apps import infographics

def open_browser():
      webbrowser.open_new('http://127.0.0.1:8050/')



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
             [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/map':
        return map.layout
    elif pathname == '/':
        return home.layout
    elif pathname == '/chart':
        return chart.layout
    elif pathname == '/infographics':
        return infographics.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
    Timer(1, open_browser).start()