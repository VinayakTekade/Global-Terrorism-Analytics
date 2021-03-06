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
from app import app
from datetime import datetime

terrorism = pd.read_csv('apps/data/global_terror_2.csv',
                        encoding = "ISO-8859-1", low_memory=False,
                        )

terrorism = terrorism[terrorism['imonth'] != 0]
terrorism['day_clean'] = [15 if x == 0 else x for x in terrorism['iday']]
terrorism['date'] = [datetime(y, m, d) for y, m, d in
                     zip(terrorism['iyear'], terrorism['imonth'], terrorism['day_clean'])]

from app import app

layout = html.Div([


        html.Div([
            html.Div([
                dcc.RangeSlider(id='years_deaths',
                                min=1970,
                                max=2016,
                                dots=True,
                                value=[1970, 2005],
                                marks={str(yr): str(yr) for yr in range(1970, 2017, 5)}),
                html.Br(),

            ], style={'margin-left': '5%', 'margin-right': '5%'}),

            dcc.Graph(id='line_country',
                      config={'displayModeBar': False},

                      )

        ], style={'width': '100%', 'float': 'left'})
    ]),


@app.callback(Output('line_country', 'figure'),
              [Input('years_deaths', 'value')])
def top_countries_deaths(years):
    df_top_countries = terrorism[terrorism['iyear'].between(years[0], years[1])]
    df_top_countries = df_top_countries.groupby(['country_txt'], as_index=False)['nkill'].agg(['count', 'sum'])

    return {
        'data': [go.Scatter(y=df_top_countries.sort_values(['sum']).tail(20)['sum'],
                        x=df_top_countries.sort_values(['sum']).tail(20).index,
                        mode = 'lines'

)],
        'layout': go.Layout(title='Total Deaths from Terrorist Attacks ' + '  ' + ' - '.join([str(y) for y in years]),
                            plot_bgcolor='#eeeeee',
                            font={'family': 'Palatino'},
                            paper_bgcolor='#eeeeee',
                            height=700,
                            yaxis={'visible': True})
    }