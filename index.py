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
from apps import horizontal_bar
from apps import densitygraph
from apps import line_country
from apps import line_region

def open_browser():
      webbrowser.open_new('http://127.0.0.1:8050/')



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
             [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/map':
        return map.layout
    elif pathname == '/chart':
        return chart.layout
    elif pathname == '/infographics':
        return infographics.layout
    elif pathname == '/horizontalbar':
        return horizontal_bar.layout
    elif pathname == '/densitygraph':
        return densitygraph.layout
    elif pathname == '/linecountry':
        return line_country.layout
    elif pathname == '/lineregion':
        return line_region.layout
    else:
        return '404'

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=True)