# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheets])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dcc.Tabs(id='navTabs', value='tab-1', children=[
                dcc.Tab(label='Home', className='navTabLink',selected_className='navTabLink--selected', value='tab-1'),
                dcc.Tab(label='Map', className='navTabLink',selected_className='navTabLink--selected', value='tab-2'),
                dcc.Tab(label='Chart', className='navTabLink',selected_className='navTabLink--selected', value='tab-3'),
                dcc.Tab(label='Infographics', className='navTabLink',selected_className='navTabLink--selected', value='tab-4'),
            ])
        ),
    ],
    brand="Logo",
    brand_href="#",
    color="white",
    dark=False,
)

app.layout = html.Div(children=[
    navbar
])

if __name__ == '__main__':
    app.run_server(debug=True)