
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
from app import app
import dash_bootstrap_components as dbc


terrorism = pd.read_csv('apps/data/global_terror_2.csv',
                        encoding='latin-1', low_memory=False,
                        )

terrorism = terrorism[terrorism['imonth'] != 0]
terrorism['day_clean'] = [15 if x == 0 else x for x in terrorism['iday']]
terrorism['date'] = [pd.datetime(y, m, d) for y, m, d in
                     zip(terrorism['iyear'], terrorism['imonth'], terrorism['day_clean'])]




layout =  html.Div([
    # html.Div([
    #     dcc.Dropdown(id='countries', className='dropdown',
    #                  multi=True,
    #                  value=[''],
    #                  placeholder='Select Countries',
    #                  options=[{'label': c, 'value': c}
    #                           for c in sorted(terrorism['country_txt'].unique())])
    # ], style={'width': '100%'}),


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
                        

    html.Br(),
    html.Br(),



], className="visualisation align-middle"),










@app.callback(Output('density', 'figure'),
              [ Input('years', 'value'),
               ])
def countries_on_map( years):
    df = terrorism[terrorism['iyear'].between(years[0], years[1])]
    fig = go.Figure(go.Densitymapbox(lat=[x + random.gauss(0.04, 0.03) for x in df[(df['iyear'].between(years[0],years[1])) ]['latitude']],
                                     lon=[x + random.gauss(0.04, 0.03) for x in df[(df['iyear'].between(years[0],years[1])) ]['longitude']],
                                     radius=10))
    fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=120)
    fig.update_layout(autosize=True,
            margin=dict(l=0, r=0, t=25, b=20),)
    # fig.show()

    return  fig
