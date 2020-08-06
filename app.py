# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from apps import map

from dash.dependencies import Input, Output

terrorism = pd.read_csv('apps/data/global_terror_2.csv',
                        encoding='latin-1', low_memory=False,
                        usecols=['iyear', 'imonth', 'iday', 'country_txt', 'city', 'longitude', 'latitude',
                        'nkill', 'gname','region_txt','provstate'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheets])

server = app.server
app.config.suppress_callback_exceptions = True

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
    color="light",
    dark=False,
)

app.layout = html.Div(children=[
    navbar,
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('navTabs', 'value')])


def render_content(tab):

    if tab == 'tab-1':
        return html.Div(className='container', children=[
            html.Img(className='militaryImg', src=app.get_asset_url('military.jpeg'))
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Div(className='row mx-3', children=[
                html.Div(className='col-3 sidebar', children=[
                    # html.H3('Side Bar')


                    # Input dropdown for Map tool goes here
                    html.Div(map.dropdown)



                ]),
                html.Div(className='col-9 visualisation', children=[
                    # html.H3('Visualisation')


                    # Output graph for Map tool goes here along with year slider
                    html.Div(map.graph)



                
                ]),
            ])
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.Div(className='row mx-3', children=[
                html.Div(className='col-3 sidebar', children=[
                    # html.H3('Side Bar')


                    # Input dropdown for Chart tool goes here 



                
                ]),
                html.Div(className='col-9 visualisation', children=[
                    # html.H3('Visualisation')


                    # Output graph for Map tool goes here 



                
                ]),
            ])
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.Div(className='row mx-3', children=[
                html.Div(className='col-3 sidebar', children=[
                    # html.H3('Side Bar')


                    # Input dropdown for Infographics Page goes here 



                
                ]),
                html.Div(className='col-9 visualisation', children=[
                    # html.H3('Visualisation')


                    # Output graph for Infographics Page goes here 



                
                ]),
            ])
        ])

        

if __name__ == '__main__':
    app.run_server(debug=True)