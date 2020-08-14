import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

pd.options.mode.chained_assignment = None


df=pd.read_csv("apps/data/global_terror_2.csv",encoding='latin-1')
df['Weapon'] = df.groupby(['weaptype1_txt','country_txt','region_txt'])['weaptype1_txt'].transform('count')
data = df.filter(['country_txt','Weapon','region_txt','weaptype1_txt']).drop_duplicates()
   
piechart =px.pie(
            data_frame=data,
            names=data['weaptype1_txt'],
            hole=.3
             )


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
        dbc.NavItem(dbc.NavLink("Weapon Type Analytics", href="/weaponType")),
        dbc.NavItem(dbc.NavLink("Death Pattern per year", href="/deathPattern")),
        dbc.NavItem(dbc.NavLink("Attacks Types used per year", href="/AttackType"))

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
                               value=[ ])
                ]),
        html.Div([dcc.Dropdown(id='country', className='dropdown',
                               multi=True,
                               placeholder='Select Country',
                               options=[{'label': c , 'value': c} for c in sorted(df['country_txt'].unique())],
                               value=[ ])
                               ]), 
        dbc.Button("Submit", outline=True, color="primary", className="dropdown d-flex justify-self-center justify-content-center", id='submit-button-state', n_clicks=0),

        dcc.Graph(id = 'pie-chart',figure=piechart)
        ])
    ])
])

@app.callback(Output('pie-chart','figure'),
            [Input('submit-button-state', 'n_clicks')],
              [State('region','value'),
               State('country','value')
              ]
              )

def update_fig(n_clicks, region_val,country_val):
    
    if((n_clicks)):

        df['Weapon'] = df.groupby(['weaptype1_txt','country_txt','region_txt'])['weaptype1_txt'].transform('count')
        data = df.filter(['country_txt','Weapon','region_txt','weaptype1_txt']).drop_duplicates()
    
        data=data[(data['country_txt'].isin(country_val)) & (data['region_txt'].isin(region_val))]

        piechart=px.pie(
            data_frame=data,
            values=data['Weapon'],
            names=data['weaptype1_txt'],
            hole=.3,
            )
    
    else:
        data =df

        piechart=px.pie(
            data_frame=data,
            names=data['weaptype1_txt'],
            hole=.3,
            )
    
            
    piechart.update_traces(textposition='inside')
    piechart.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    return (piechart)