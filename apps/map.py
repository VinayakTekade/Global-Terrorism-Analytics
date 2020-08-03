import random
import textwrap
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from app import app
import dash_bootstrap_components as dbc

terrorism = pd.read_csv('apps/data/global_terror.csv',
                        encoding='latin-1', low_memory=False,
                        usecols=['iyear', 'imonth', 'iday', 'country_txt', 'city', 'longitude', 'latitude',
                        'nkill', 'nwound', 'summary', 'target1', 'gname','region_txt','provstate'])

terrorism = terrorism[terrorism['imonth'] != 0]
terrorism['day_clean'] = [15 if x == 0 else x for x in terrorism['iday']]
terrorism['date'] = [pd.datetime(y, m, d) for y, m, d in zip(terrorism['iyear'], terrorism['imonth'], terrorism['day_clean'])]
########################################################################################################################







# we use a callback to toggle the collapse on small screens



# the same function (toggle_navbar_collapse) is used in all three callbacks
#











# selection tools
#years
layout = html.Div([


    html.Div([
        html.Div([
            html.Div([
                html.H1("Global Terrorism Data Visualization")
            ], className="branding"),

            html.Div([
                html.Div(
                    className="A",
                    children=[
                        html.Ul(className='my-list', children=[html.Li(html.A('Map Tool', href='/country')),
                                                               html.Li(html.A('Chart Tool', href='/')),
                                                               html.Li(html.A('Infographics', href='/'))])
                    ],
                )
            ], className='nav')
        ], className="container"),

    ], className="header"),
    html.Br(),

#month
    html.Div([
        dcc.Dropdown(id='month',
                     multi=True,
                     value=[''],
                     placeholder='Select Month',
                     options=[{'label': c, 'value': c}
                              for c in sorted(terrorism['imonth'].unique())])
    ], style={'width': '50%', 'margin-left': '25%', 'background-color': '#eeeeee'}),

#date
    html.Div([
        dcc.Dropdown(id='date',
                     multi=True,
                     value=[''],
                     placeholder='Select Date',
                     options=[{'label': c, 'value': c}
                              for c in sorted(terrorism['iday'].unique())])
    ], style={'width': '50%', 'margin-left': '25%', 'background-color': '#eeeeee'}),


#region
    html.Div([
        dcc.Dropdown(id='region',
                     multi=True,
                     value=[''],
                     placeholder='Select region',
                     options=[{'label': c, 'value': c}
                              for c in sorted(terrorism['region_txt'].unique())])
    ], style={'width': '50%', 'margin-left': '25%', 'background-color': '#eeeeee'}),



#countries
    html.Div([
        dcc.Dropdown(id='countries',
                     multi=True,
                     value=[''],
                     placeholder='Select Countries',
                     options=[{'label': c, 'value': c}
                              for c in sorted(terrorism['country_txt'].unique())])
    ], style={'width': '50%', 'margin-left': '25%', 'background-color': '#eeeeee'}),

#City
    html.Div([
        html.Div([
            dcc.Dropdown(id='provstate',
                         multi=True,
                         value=[''],
                         placeholder='States / Provinces / Districts',
                         options = [{'label': prov, 'value': prov}
            for prov in sorted(terrorism[terrorism['provstate'].notna()]['provstate'].unique())])
        ], style={'width': '40%', 'display': 'inline-block', }),
        html.Div([
            dcc.Dropdown(id='cities',
                         multi=True,
                         value=[''],
                         placeholder='Cities',
                         options = [{'label': prov, 'value': prov}
            for prov in sorted(terrorism[terrorism['city'].notna()]['city'].unique())])
        ], style={'width': '40%', 'display': 'inline-block', })
    ], style={'width': '80%', 'margin-left': '20%'}),





    dcc.Graph(id='map_world',
              config={'displayModeBar': False}),

    html.Div([
        dcc.RangeSlider(id='years',
                        min=1970,
                        max=2018,
                        dots=True,
                        value=[1970, 2000],
                        marks={str(yr): "'" + str(yr)[2:] for yr in range(1970, 2019)}),

        html.Br(),
        html.Br(),

    ], style={'width': '75%', 'margin-left': '12%', 'background-color': '#eeeeee'}),

])
#####################################################################################################################################
#functions for the selection tools

@app.callback(Output('map_world', 'figure'),
              [Input('countries', 'value'), Input('years', 'value'), Input('region', 'value') , Input('month', 'value'), Input('date', 'value'), Input('provstate', 'value'), Input('cities', 'value')])
def countries_on_map(countries, years, region, month, date, cities, provstate):
    df = terrorism[terrorism['country_txt'].isin(countries) & terrorism['iyear'].between(years[0], years[1]) & terrorism['region_txt'].isin(region) & terrorism['imonth'].isin(month) & terrorism['iday'].isin(date)  & terrorism['city'].isin(cities) | terrorism['provstate'].isin(provstate)]

    return {
        'data': [go.Scattergeo(lon=[x + random.gauss(0.04, 0.03) for x in df[df['country_txt'] == c]['longitude']],
                               lat=[x + random.gauss(0.04, 0.03) for x in df[df['country_txt'] == c]['latitude']],
                               name=c,
                               hoverinfo='text',
                               mode= 'markers',


                               marker={'size': 9, 'opacity': 0.65, 'line': {'width': .2, 'color': '#cccccc'}},
                               hovertext=df[df['country_txt'] == c]['city'].astype(str) + ', ' +
                                         df[df['country_txt'] == c]['country_txt'].astype(str) + '<br>' +
                                         [dt.datetime.strftime(d, '%d %b, %Y') for d in
                                          df[df['country_txt'] == c]['date']] + '<br>' +
                                         'Perpetrator: ' + df[df['country_txt'] == c]['gname'].astype(str) + '<br>' +
                                         'Target: ' + df[df['country_txt'] == c]['target1'].astype(str) + '<br>' +
                                         'Deaths: ' + df[df['country_txt'] == c]['nkill'].astype(str) + '<br>' +
                                         'Injured: ' + df[df['country_txt'] == c]['nwound'].astype(str) + '<br><br>' +
                                         ['<br>'.join(textwrap.wrap(x, 40)) if not isinstance(x, float) else '' for x in
                                          df[df['country_txt'] == c]['summary']])
                 for c in countries],

        'layout': go.Layout(
            title='Terrorist Attacks ' + ', '.join(countries) + '  ' + ' - '.join([str(y) for y in years]),
            font={'family': 'Palatino'},
            titlefont={'size': 22},
            paper_bgcolor='#ffffff',
            plot_bgcolor='#eeeeee',
            width=1420,
            height=650,


            geo={'showland': True, 'landcolor': '#eeeeee',
                 'countrycolor': '#cccccc',
                 'showsubunits': True,
                 'subunitcolor': '#cccccc',
                 'subunitwidth': 5,
                 'showcountries': True,
                 'oceancolor': '#e9f5f7',
                 'showocean': True,
                 'showcoastlines': True,
                 'showframe': False,
                 'coastlinecolor': '#cccccc',
                 'lonaxis': {'range': [df['longitude'].min() - 1, df['longitude'].max() + 1]},
                 'lataxis': {'range': [df['latitude'].min() - 1, df['latitude'].max() + 1]}
                 })
    }

