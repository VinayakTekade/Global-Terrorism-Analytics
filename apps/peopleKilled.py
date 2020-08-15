import random
import textwrap
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
pd.options.mode.chained_assignment = None
import dash_bootstrap_components as dbc
from app import app

terrorism = pd.read_csv('apps/data/global_terror_2.csv',
                        encoding='latin-1', low_memory=False,
                        )

terrorism = terrorism[terrorism['imonth'] != 0]
terrorism['day_clean'] = [15 if x == 0 else x for x in terrorism['iday']]
terrorism['date'] = [pd.datetime(y, m, d) for y, m, d in
                     zip(terrorism['iyear'], terrorism['imonth'], terrorism['day_clean'])]

from app import app

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Map", href="/map")),
        dbc.NavItem(dbc.NavLink("Chart", href="/chart")),
        dbc.NavItem(dbc.NavLink("Infographics", href="#"), className='selected')
    ],
    brand="Global Terrorism Data Visualization",
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
               dcc.Graph(id='top_countries_deaths',
                        className="plot",
                        config={'displayModeBar': False},
                        
                    ),

                html.Div([
                    dcc.RangeSlider(id='years_deaths',
                                    min=1970,
                                    max=2016,
                                    dots=True,
                                    value=[1970, 2005],
                                    marks={str(yr): str(yr) for yr in range(1970, 2017, 5)}
                                    )
                ], className="rangeSlider")
        ])
    ])
])


@app.callback(Output('top_countries_deaths', 'figure'),
              [Input('years_deaths', 'value')])
def top_countries_deaths(years):
    df_top_countries = terrorism[terrorism['iyear'].between(years[0], years[1])]
    df_top_countries = df_top_countries.groupby(['region_txt'], as_index=False)['nkill'].agg(['count', 'sum'])

    return {
        'data': [go.Bar(x=df_top_countries.sort_values(['sum']).tail(20)['sum'],
                        y=df_top_countries.sort_values(['sum']).tail(20).index,
                        orientation='h',
                        constraintext='none',
                        showlegend=False,
                        text=df_top_countries.sort_values(['sum']).tail(20).index,
                        textposition='inside'
                        )],
        'layout': go.Layout(title='Total Deaths from Terrorist Attacks ' + '  ' + ' - '.join([str(y) for y in years]),
                            plot_bgcolor='#eeeeee',
                            font={'family': 'Palatino'},
                            paper_bgcolor='#ffffff',
                            barmode='stack',
                            yaxis={'visible': False},
                            margin=dict(l=0, r=0, t=25, b=50),
                        )
    }