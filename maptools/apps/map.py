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

terrorism = pd.read_csv('apps/data/global_terror.csv',
                        encoding='latin-1', low_memory=False,
                        usecols=['iyear', 'imonth', 'iday', 'country_txt', 'city', 'longitude', 'latitude',
                        'nkill', 'nwound', 'summary', 'target1', 'gname','region_txt','provstate', 'attacktype1_txt'])

terrorism = terrorism[terrorism['imonth'] != 0]
terrorism['day_clean'] = [15 if x == 0 else x for x in terrorism['iday']]
terrorism['date'] = [pd.datetime(y, m, d) for y, m, d in zip(terrorism['iyear'], terrorism['imonth'], terrorism['day_clean'])]
terrorism['month_txt'] = pd.DataFrame([calendar.month_name[i] for i in terrorism['imonth']]).astype(str)
########################################################################################################################







# we use a callback to toggle the collapse on small screens



# the same function (toggle_navbar_collapse) is used in all three callbacks
#

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/home")),
        dbc.NavItem(dbc.NavLink("Map", href="#")),
        dbc.NavItem(dbc.NavLink("Chart", href="/chart")),
        dbc.NavItem(dbc.NavLink("Infographics", href="/infographics")),
    ],
    brand="Global Terrorism Data Visualization",
    brand_href="#",
    color="light",
    dark=False,
)








# selection tools
#years
layout = html.Div([


    navbar,

   html.Div(className='row mx-3', children=[
                html.Div(className='col-3 sidebar', children=[
                    html.Div([
        dcc.Dropdown(id='month', className='dropdown',
                     multi=True,
                     value=[''],
                     placeholder='Select Month',
                     options=[{'label': c, 'value': c}
                              for c in sorted(terrorism[terrorism['month_txt'].notna()]['month_txt'].unique())])
    ]),

    # date
    html.Div([
        dcc.Dropdown(id='date', className='dropdown',
                     multi=True,
                     value=[''],
                     placeholder='Select Date',
                     options=[{'label': c, 'value': c}
                              for c in sorted(terrorism['iday'].unique())])
    ]),

    # region
    html.Div([
        dcc.Dropdown(id='region', className='dropdown',
                     multi=True,
                     value=[''],
                     placeholder='Select region',
                     options=[{'label': c, 'value': c}
                              for c in sorted(terrorism['region_txt'].unique())])
    ]),

    # countries
    html.Div([
        dcc.Dropdown(id='countries', className='dropdown',
                     multi=True,
                     value=[''],
                     placeholder='Select Countries',
                     options=[{'label': c, 'value': c}
                              for c in sorted(terrorism['country_txt'].unique())])
    ]),

    # City

    html.Div([
        dcc.Dropdown(id='provstate', className='dropdown',
                     multi=True,
                     value=[''],
                     placeholder='States / Provinces / Districts',
                     options=[{'label': prov, 'value': prov}
                              for prov in sorted(terrorism[terrorism['provstate'].notna()]['provstate'].unique())])
    ]),
    html.Div([
        dcc.Dropdown(id='cities', className='dropdown',
                     multi=True,
                     value=[''],
                     placeholder='Cities',
                     options=[{'label': prov, 'value': prov}
                              for prov in sorted(terrorism[terrorism['city'].notna()]['city'].unique())])
    ])
                ]),
                html.Div(className='col-9 visualisation', children=[
                     dcc.Graph(id='map_world',
              config={'displayModeBar': False}),

    html.Div([
        dcc.RangeSlider(id='years',
                        min=1970,
                        max=2018,
                        dots=True,
                        value=[2010, 2018],
                        marks={str(yr): "'" + str(yr)[2:] for yr in range(1970, 2019)}),

        html.Br(),
        html.Br(),

    ])
                ])
])
])




#####################################################################################################################################
#functions for the selection tools

@app.callback(Output('map_world', 'figure'),
              [Input('countries', 'value'), Input('years', 'value'), Input('region', 'value') , Input('month', 'value'), Input('date', 'value'), Input('provstate', 'value'), Input('cities', 'value')])
def countries_on_map(countries, years, region, month, date, cities, provstate):
    df = terrorism[terrorism['country_txt'].isin(countries) & terrorism['iyear'].between(years[0], years[1])]

    return {
        'data': [go.Scattergeo(lon=[x + random.gauss(0.04, 0.03) for x in df[(df['country_txt'] == c) & (df['iyear'].between(years[0],years[1])) ]['longitude']],
                               lat=[x + random.gauss(0.04, 0.03) for x in df[(df['country_txt'] == c) & (df['iyear'].between(years[0],years[1]))]['latitude']],
                               name=c,
                               hoverinfo='text',
                               mode= 'markers',



                               marker={'size': 9, 'opacity': 0.65, 'line': {'width': .2, 'color': '#cccccc'}},
                               hovertext=df[(df['country_txt'] == c) & (df['iyear'].between(years[0],years[1]))]['city'].astype(str) + ', ' +
                                         df[(df['country_txt'] == c) & (df['iyear'].between(years[0],years[1]))]['country_txt'].astype(str) + '<br>' +
                                         [dt.datetime.strftime(d, '%d %b, %Y') for d in
                                          df[(df['country_txt'] == c) & (df['iyear'].between(years[0],years[1]))]['date']] + '<br>' +
                                         'Region: ' + df[df['country_txt'] == c ]['region_txt'].astype(str) + '<br>' +
                                         'Attacktype: ' + df[df['country_txt'] == c]['attacktype1_txt'].astype(str) + '<br>' +
                                         'Perpetrator: ' + df[(df['country_txt'] == c) & (df['iyear'].between(years[0],years[1]))]['gname'].astype(str) + '<br>' +
                                         'Target: ' + df[(df['country_txt'] == c) & (df['iyear'].between(years[0],years[1]))]['target1'].astype(str) + '<br>' +
                                         'Deaths: ' + df[(df['country_txt'] == c) & (df['iyear'].between(years[0],years[1]))]['nkill'].astype(str) + '<br>' +
                                         'Injured: ' + df[(df['country_txt'] == c) & (df['iyear'].between(years[0],years[1]))]['nwound'].astype(str) + '<br><br>' +
                                         ['<br>'.join(textwrap.wrap(x, 40)) if not isinstance(x, float) else '' for x in
                                          df[(df['country_txt'] == c) & (df['iyear'].between(years[0],years[1]))]['summary']])
                 for c in countries]+
                [go.Scattergeo(lon=[x + random.gauss(0.04, 0.03) for x in df[df['provstate'] == c]['longitude']],
                               lat=[x + random.gauss(0.04, 0.03) for x in df[df['provstate'] == c]['latitude']],
                               name=c,
                               hoverinfo='text',
                               opacity=0.9,
                               marker={'size': 9, 'line': {'width': .2, 'color': '#cccccc'}},
                               hovertext=df[(df['provstate'] == c) & (df['iyear'].between(years[0],years[1]))]['city'].astype(str) + ', ' +
                                         df[(df['provstate'] == c) & (df['iyear'].between(years[0],years[1]))]['country_txt'].astype(str) + '<br>' +
                                         [dt.datetime.strftime(d, '%d %b, %Y') for d in
                                          df[(df['provstate'] == c) & (df['iyear'].between(years[0],years[1]))]['date']] + '<br>' +
                                         'Region: ' + df[df['provstate'] == c ]['region_txt'].astype(str) + '<br>' +
                                         'Attacktype: ' + df[df['provstate'] == c]['attacktype1_txt'].astype(str) + '<br>' +
                                         'Perpetrator: ' + df[(df['provstate'] == c) & (df['iyear'].between(years[0],years[1]))]['gname'].astype(str) + '<br>' +
                                         'Target: ' + df[(df['provstate'] == c) & (df['iyear'].between(years[0],years[1]))]['target1'].astype(str) + '<br>' +
                                         'Deaths: ' + df[(df['provstate'] == c) & (df['iyear'].between(years[0],years[1]))]['nkill'].astype(str) + '<br>' +
                                         'Injured: ' + df[(df['provstate'] == c) & (df['iyear'].between(years[0],years[1]))]['nwound'].astype(str) + '<br><br>' +
                                         ['<br>'.join(textwrap.wrap(x, 40)) if not isinstance(x, float) else '' for x in
                                          df[(df['provstate'] == c) & (df['iyear'].between(years[0],years[1]))]['summary']])
                 for c in provstate] +

                [go.Scattergeo(lon=[x + random.gauss(0.04, 0.03) for x in df[df['city'] == c]['longitude']],
                               lat=[x + random.gauss(0.04, 0.03) for x in df[df['city'] == c]['latitude']],
                               name=c,
                               hoverinfo='text',
                               opacity=0.9,
                               marker={'size': 9, 'line': {'width': .2, 'color': '#cccccc'}},
                               hovertext=df[(df['city'] == c) & (df['iyear'].between(years[0],years[1]))]['city'].astype(str) + ', ' +
                                         df[(df['city'] == c) & (df['iyear'].between(years[0],years[1]))]['country_txt'].astype(str) + '<br>' +
                                         [dt.datetime.strftime(d, '%d %b, %Y') for d in
                                          df[(df['city'] == c) & (df['iyear'].between(years[0],years[1]))]['date']] + '<br>' +
                                         'Region: ' + df[df['city'] == c ]['region_txt'].astype(str) + '<br>' +
                                         'Attacktype: ' + df[df['city'] == c]['attacktype1_txt'].astype(str) + '<br>' +
                                         'Perpetrator: ' + df[(df['city'] == c) & (df['iyear'].between(years[0],years[1]))]['gname'].astype(str) + '<br>' +
                                         'Target: ' + df[(df['city'] == c) & (df['iyear'].between(years[0],years[1]))]['target1'].astype(str) + '<br>' +
                                         'Deaths: ' + df[(df['city'] == c) & (df['iyear'].between(years[0],years[1]))]['nkill'].astype(str) + '<br>' +
                                         'Injured: ' + df[(df['city'] == c) & (df['iyear'].between(years[0],years[1]))]['nwound'].astype(str) + '<br><br>' +
                                         ['<br>'.join(textwrap.wrap(x, 40)) if not isinstance(x, float) else '' for x in
                                          df[(df['city'] == c) & (df['iyear'].between(years[0],years[1]))]['summary']])
                 for c in cities],

        'layout': go.Layout(
            title='Terrorist Attacks ' + ', '.join(countries) + '  ' + ' - '.join([str(y) for y in years]),
            font={'family': 'Palatino'},
            titlefont={'size': 22},
            paper_bgcolor='#ffffff',
            plot_bgcolor='#eeeeee',
            width=1000,
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
