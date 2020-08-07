import dash
import dash_html_components as html
from app import app
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


terrorism = pd.read_csv('apps/data/global_terror_2.csv',
                        encoding='latin-1', low_memory=False,
                        )

terrorism = terrorism[terrorism['imonth'] != 0]
terrorism['day_clean'] = [15 if x == 0 else x for x in terrorism['iday']]
terrorism['date'] = [pd.datetime(y, m, d) for y, m, d in
                     zip(terrorism['iyear'], terrorism['imonth'], terrorism['day_clean'])]
catogories = [ 'country_txt',
       'region_txt',
       'attacktype1_txt', 'weaptype1_txt',
       'targtype1_txt', 'gname','natlty1_txt'],

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Map", href="/map")),
        dbc.NavItem(dbc.NavLink("Chart", href="#"), className='selected'),
        dbc.NavItem(dbc.NavLink("Infographics", href="/infographics")),
    ],
    brand="Global Terrorism Data Visualization",
    brand_href="#",
    color="light",
    dark=False,
    className="navbar",
    fluid=True
)

layout = html.Div([
    navbar,
    html.Div(className='container', children=[
            html.H3('Chart page'),
    html.Div([
        dcc.Dropdown(id='categories',

                     value=[''],
                     placeholder='Select category',
                     options=[{'label': 'Country', 'value': 'country_txt'},
                              {'label': 'Region', 'value': 'region_txt'},
                              {'label': 'Type of attack', 'value': 'attacktype1_txt'},
                              {'label': 'Weapon type', 'value': 'weaptype1_txt'},
                              {'label': 'Target name', 'value': 'targtype1_txt'},
                              {'label': 'Organization name', 'value': 'gname'},
                              {'label': 'Nationality', 'value': 'natlty1_txt'},
                              ])
    ], style={'width': '50%', 'margin-left': '25%', 'background-color': '#ffffff'}),

    dcc.Graph(id='by_year_country_world',
              config={'displayModeBar': False}),
    html.Hr(),

    html.Div([
        dcc.RangeSlider(id='years',
                        min=1970,
                        max=2018,
                        dots=True,
                        value=[2010, 2018],
                        marks={str(yr): "'" + str(yr)[2:] for yr in range(1970, 2019)}),

        html.Br(), html.Br(),
    ], style={'width': '75%', 'margin-left': '12%', 'background-color': '#ffffff'}),
        ])
])


@app.callback(Output('by_year_country_world', 'figure'),
              [ Input('years', 'value'),Input('categories', 'value')])
def chat_tool(years, categories1):
    categary = terrorism[categories1].unique()
    df = terrorism[terrorism[categories1].isin(categary) & terrorism['iyear'].between(years[0], years[1])]
    df = df.groupby(['iyear', categories1], as_index=False)['date'].count()

    return {
        'data': [go.Scatter(x=df[df[categories1] == c]['iyear'],
                            y=df[df[categories1] == c]['date'],
                            name=c,
                            mode='lines',

                            )
                 for c in categary],
        'layout': go.Layout(
            title='Yearly Terrorist Attacks Catogory wise  ' + ' - '.join([str(y) for y in years]),
            plot_bgcolor='#eeeeee',
            paper_bgcolor='#eeeeee',
            font={'family': 'Palatino'})
    }

