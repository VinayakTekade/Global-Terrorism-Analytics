import random
import textwrap
import datetime as dt
import calendar
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
pd.options.mode.chained_assignment = None
from app import app
import dash_bootstrap_components as dbc
from datetime import datetime

terrorism = pd.read_csv('apps/data/global_terror_2.csv',
                        encoding = "ISO-8859-1", low_memory=False,
                        )

terrorism = terrorism[terrorism['imonth'] != 0]
terrorism['day_clean'] = [15 if x == 0 else x for x in terrorism['iday']]
terrorism['date'] = [datetime(y, m, d) for y, m, d in
                     zip(terrorism['iyear'], terrorism['imonth'], terrorism['day_clean'])]


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Map", href="/map")),
        dbc.NavItem(dbc.NavLink("Chart", href="/chart")),
        dbc.NavItem(dbc.NavLink("Infographics", href="#"), className='selected')
    ],
    brand="Global Terrorism Analytics",
    brand_href="#",
    color="light",
    dark=False,
    className="navbar",
    fluid=True
)


nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Intensity of Attacks", href="/densityGraph")),
        dbc.NavItem(dbc.NavLink("Comparison of Attack Types", href="/compAttack")),
        dbc.NavItem(dbc.NavLink("People killed per Region", href="/peopleKilled")),
        dbc.NavItem(dbc.NavLink("Weapon Type Analytics", href="/weaponUsed")),
        dbc.NavItem(dbc.NavLink("Death Pattern per year", href="/deathPattern")),
        dbc.NavItem(dbc.NavLink("Attacks Types used per year", href="/attackType"))

    ]
)


layout = html.Div([


    navbar,

    html.Div(className='row mx-3', children=[
        html.Div(className='col-3 sidebar', children=[   
                nav
        ]),
    
        html.Div(className='col-9 visualisation align-middle', children=[
            
            dcc.Graph(id='density', className="plot",
                    config={'displayModeBar': False},
              ),

            html.Div([
                    dcc.RangeSlider(id='years',
                                    min=1970,
                                    max=2018,
                                    dots=True,
                                    value=[1970, 2018],
                                    marks={str(yr): "'" + str(yr)[2:] for yr in range(1970, 2019)}),
                ], className="rangeSlider"),

        ])
    ])
])


@app.callback(Output('density', 'figure'),
              [ Input('years', 'value'),
               ])
def countries_on_map( years):
    df = terrorism[terrorism['iyear'].between(years[0], years[1])]
    fig = go.Figure(go.Densitymapbox(lat=[x + random.gauss(0.04, 0.03) for x in df[(df['iyear'].between(years[0],years[1])) ]['latitude']],
                                     lon=[x + random.gauss(0.04, 0.03) for x in df[(df['iyear'].between(years[0],years[1])) ]['longitude']],
                                     radius=10))
    fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=120, autosize=True, margin=dict(l=0, r=0, t=25, b=20))
    # fig.show()

    return  fig
