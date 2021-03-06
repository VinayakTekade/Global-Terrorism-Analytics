
import flask                                               # pip install Flask
import pandas as pd
pd.options.mode.chained_assignment = None                                        # pip install pandas
import dash                                                # pip install dash
import dash_core_components as dcc                          #pip install dash-core-components
import dash_html_components as html                         # pip install dash-html-components
from dash.dependencies import Input, State, Output           # pip install dash-renderer
import plotly.graph_objects as go                            #pip install plotly
import plotly.express as px
import dash_table as dt  
import dash_table
import dash_bootstrap_components as dbc                     #pip install dash-bootstrap-components
import os
import math
from app import app


#Create dataframe of reduced csv
df = pd.read_csv("apps/data/global_terror_2.csv",encoding = "ISO-8859-1")
filter_options = ['Property Damage', 'Target Nationality', 'Target Type', 'Type of Attack', 'Weapon Type', 'Region', 'Country']
fig50  = None

def navbar_ui():
    """
    Displays navbar
    """
    navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Map", href="/map")),
        dbc.NavItem(dbc.NavLink("Chart", href="#"), className='selected'),
        dbc.NavItem(dbc.NavLink("Infographics", href="/infographics"))
    ],
    brand="Global Terrorism Analytics",
    brand_href="#",
    color="light",
    dark=False,
    className="navbar",
    fluid=True
    )
    return navbar

def chart_inputs_ui():
    """
    Displays input field for chart plot
    """
    chart_filters = html.Div([
                    dcc.Dropdown(
                        id='category',
                        options=[{'label': j, 'value': i} for i, j in enumerate(filter_options)],
                        value=6,
                        clearable=False,
                        className='dropdown'
                    ),

                    html.Div([
                            dbc.Input(type="text", id='searchtext', className="dropdown", placeholder='Search'),
                            html.Div(id='msg', children="")
                    ]),
                ]),
    return chart_filters

def chart_plot_ui():
    """
    displays chart plot
    """
    plot = [dcc.Graph(id='plots3', className="plot", figure=fig50),                    
            html.Div([
                    dcc.RangeSlider(
                    id='yearslider',
                    min=1970,
                    max=2018,
                    value=[1970, 2018],
                    marks={str(yr): "'" + str(yr)[2:] for yr in range(1970, 2019, 1)},
                    allowCross=False,
                    )
            ], className="rangeSlider")
    ]       
    return plot


# Default processing of Graph
df['Attacks'] = df.groupby(['country_txt', 'iyear'])['country_txt'].transform('count')
dfr = df.filter(['country_txt', 'Attacks', 'iyear']).drop_duplicates()

fig50 = px.area(dfr, x="iyear", y="Attacks", color="country_txt", line_group="country_txt")


layout =  html.Div([
    navbar_ui(),
    html.Div([

        html.Div(className='row mx-3', children=[
            html.Div(className='col-3 sidebar', children=
                chart_inputs_ui()
            ),
            html.Div(className='col-9 visualisation align-middle', children=
                chart_plot_ui()
            )
        ])
    ])
])
#App callback and function to create GTD explorer ( world)
@app.callback(
[Output('plots3', 'figure'), Output('msg', 'children')],
[Input('category', 'value'), Input('yearslider', 'value'), Input('searchtext', 'value')]
)

def update_chart(catvalue, yrange, search):
  if catvalue==None:
      return None

  min=yrange[0]
  max=yrange[1]
  
  msg=""
  


  group = ['propextent_txt', 'natlty1_txt', 'targtype1_txt', 'attacktype1_txt', 'weaptype1_txt', 'region_txt', 'country_txt']
  

  data = df[df[group[catvalue]].notnull()]
  data['Attacks'] = data.groupby([group[catvalue], 'iyear'])[group[catvalue]].transform('count')
  data = data.filter([group[catvalue], 'Attacks', 'iyear']).drop_duplicates()
  data=data[(data['iyear']>=min) & (data['iyear']<=max)]
  
  if search!=None:
      dfr=data[data.iloc[:, 0].str.contains('^'+search, case=False, regex=True)]
      if dfr.empty==True:
          msg="No matches found!"
      else:
          data=dfr
  
  fig50 = px.area(data, x="iyear", y="Attacks", color=group[catvalue], line_group=group[catvalue])

  return fig50, msg
        





