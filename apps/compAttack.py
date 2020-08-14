
import pandas as pd
import plotly.graph_objects as go
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
pd.options.mode.chained_assignment = None

terror=pd.read_csv("apps/data/global_terror_2.csv",encoding='latin-1')
# print(terror.head())
terror['Attack'] = terror.groupby(['country_txt', 'region_txt'])['attacktype1_txt'].transform('count')
df = terror.filter(['country_txt', 'region_txt', 'Attack','attacktype1_txt','iyear']).drop_duplicates()
#print(df)

fig={}

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
               html.Div([dcc.Dropdown(id='region', className='dropdown',
                               placeholder='Select Region',
                               multi=True,
                               options=[{'label': c , 'value': c} for c in sorted(df['region_txt'].unique())],
                               value=[''])
                ]),
                html.Div([dcc.Dropdown(id='country', className='dropdown',
                               multi=True,
                               placeholder='Select Country',
                               options=[{'label': c , 'value': c} for c in sorted(df['country_txt'].unique())],
                               value=[''])
                ]),
                dbc.Button("Submit", outline=True, color="primary", className="dropdown d-flex justify-self-center justify-content-center", id='submit-button-state', n_clicks=0),
                dcc.Graph(id = 'stack-bargraph',figure=fig)
        ])
    ])
])

@app.callback(Output('stack-bargraph','figure'),
                [Input('submit-button-state', 'n_clicks')],
              [State('region','value'),
               State('country','value')
              ]
              )

def update_fig(n_clicks, region_val, country_val):
    if(n_clicks):
        terror['Attack'] = terror.groupby(['country_txt', 'region_txt'])['attacktype1_txt'].transform('count')
        data = terror.filter(['country_txt', 'region_txt','attacktype1_txt','Attack','iyear']).drop_duplicates()
        data=data[(data['country_txt'].isin(country_val)) & (data['region_txt'].isin(region_val))]

        traces=[go.Bar(
        x=data.iyear,
        y=data.Attack,
        name=c 
        )for c in data['attacktype1_txt'].unique()]
        graph_layout=go.Layout(title='Comparison of Attacktypes over Years',barmode='stack')
        fig=go.Figure(data=traces,layout=graph_layout)

    else:
        terror['Attack'] = terror.groupby(['country_txt', 'region_txt'])['attacktype1_txt'].transform('count')
        df = terror.filter(['country_txt', 'region_txt', 'Attack','attacktype1_txt','iyear']).drop_duplicates()
        
        traces=[go.Bar(
            x=df.iyear,
            y=df.Attack,
            name=c 
            )for c in df['attacktype1_txt'].unique()]
        graph_layout=go.Layout(title='Comparison of Attacktypes over Years',barmode='stack')
        fig=go.Figure(data=traces,layout=graph_layout)


        
    return fig
