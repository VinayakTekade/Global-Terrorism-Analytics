
# Modules Loading
import pandas as pd

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,  Output
from app import app
import plotly.express as px
import dash_bootstrap_components as dbc

pd.options.mode.chained_assignment = None


# Data Loading
main_data = pd.read_csv("apps/data/global_terror_2.csv", encoding = "ISO-8859-1")


# Dropdown filters
month = {"January":1,
         "February": 2,
         "March": 3,
         "April":4,
         "May":5,
         "June":6,
         "July": 7,
         "August":8,
         "September":9,
         "October":10,
         "November":11,
         "December":12
         }

date = [x for x in range(1, 32)]
type_of_attacks ={'ALL': 0,
                 'Assasination': 1,
                'Armed Assault': 2,
                'Bombing/Explosion':3,
                'Hijacking': 4,
                'Barricade Incident': 5,
                 'Kidnapping' : 6,              
                 'Facility/Infrastructure Attack' :7,
                'Unarmed Assault' : 8,
                'Unknown': 9}

continent = list(main_data["region_txt"].unique())
country = main_data.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
city = main_data.groupby("country_txt")["city"].unique().apply(list).to_dict()

#Layout
def navbar_ui():
    """
    Displays navbar
    """
    navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Map", href="#"), className='selected'),
        dbc.NavItem(dbc.NavLink("Chart", href="/chart")),
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

def map_inputs_ui():
    """
    Displays input field for Map
    """
    map_filters = [
                        html.Div(
                            dcc.Dropdown(id = "month", 
                                              options=[{"label":key, "value":values} for key,values in month.items()],
                                              placeholder = "Select month"
                            ),
                            className="dropdown"
                        ),
                        
                        html.Div(
                            dcc.Dropdown(id="date", placeholder ="Select Date"
                            ),
                            className="dropdown" 
                        ),
                        
                        html.Div(
                            dcc.Dropdown(id="attack_types", 
                                              options = [{"label": keys, "value": values} for keys, values in type_of_attacks.items()],
                                              placeholder="Select Attack Types"
                            ),
                            className="dropdown"                 
                        ),
                        
                        html.Div(
                            dcc.Dropdown(id="continent" ,
                                              options = [{'label':m, 'value':m} for m in continent],
                                              placeholder="Select Continent"
                            ),
                            className="dropdown"
                                              
                        ),

                        html.Div(
                            dcc.Dropdown(id = "country",
                                        placeholder="Select Country"
                            ),
                            className="dropdown"
                        ),
                            

                        html.Div(
                            dcc.Dropdown(id = "city",
                                        placeholder="Select City"
                            ),
                            className="dropdown"            
                        ),
    ]
    return map_filters

def map_plot_ui():
    """
    Displays map plot
    """
    plot = [
            html.Div(id = "graph",
                    className="plot"
                ),
            html.Div([
                dcc.RangeSlider(id='years',
                                min=1970,
                                max=2018,
                                dots=True,
                                value=[1970, 2018],
                                marks={str(yr): "'" + str(yr)[2:] for yr in range(1970, 2019)}),
            ], className="rangeSlider")
    ]
    return plot



layout = html.Div([
    navbar_ui(),

    html.Div(className='row mx-3', children=[
                html.Div(className='col-3 sidebar', children= map_inputs_ui()),
                html.Div(className='col-9 visualisation align-middle', children= map_plot_ui())
    ])
])


# Phase2 - Callbacks
@app.callback(Output("date", "options"),
                [Input("month", "value")])
def update_date(month):
    if month in [1,3,5,7,8,10,12]:
        return [{"label":m, "value":m} for m in date]
    elif month in [4,6,9,11]:
        return [{"label":m, "value":m} for m in date[:-1]]
    elif month==2:
        return [{"label":m, "value":m} for m in date[:-2]]
    
    else:
        return []

@app.callback(Output("country", "options"),
              [Input("continent", "value")])
def update_countries(continent):
    if continent in country.keys():
        return [{'label':m, 'value':m} for m in country[continent]]
    else:
        return []

@app.callback(Output("city", "options"),
              [Input("country", "value")])
def update_cities(country):
    if country in city.keys():
        return [{'label':m, 'value':m} for m in city[country]]
    else:
        return []


def checkinput(data, continent, country, city):
    if continent and country and city:
        new_data = data[(data["region_txt"]==continent) &
                         (data["country_txt"]==country)&
                         (data["city"]==city)]
    elif continent and country:
        new_data = data[(data["region_txt"]==continent) &
                         (data["country_txt"]==country)]
        
    elif continent:
        new_data = data[(data["region_txt"]==continent)]
        
    else:
        new_data = data
    return new_data
    






##########################################################################    
@app.callback(Output("graph", "children"),
              [Input("month", "value"),
               Input("date", "value"),
               Input("attack_types", "value"),
               Input("continent", "value"),
               Input("country", "value"),
               Input("city", "value"),
               Input("years","value")
               ])
def update_graph(month, date, attack_types, continent, country, city, years):
   
    # To check for attack types 
    if attack_types == 0 :
        
        data = main_data[(main_data["imonth"]==month) &
                         (main_data["iday"]==date)]
        
        
        
    elif attack_types!=0:
        data = main_data[(main_data["imonth"]==month) &
                         (main_data["iday"]==date)&
                         (main_data["attacktype1"]==attack_types)]
    
    
    # to check for the filters of region, country and city wise
    if continent or country or city:
        data = checkinput(data, continent, country, city)
    
    
    
    
    # To check whether data is empty or not
    if data.shape[0]:
        pass
    else:
        data = main_data.iloc[[0]]
        
    min=years[0]
    max=years[1]    
    data=data[(data['iyear']>=min) & (data['iyear']<=max)]
    fig = px.scatter_mapbox(data,
                        lat="latitude", 
                        lon="longitude",
                        hover_name="city", 
                        hover_data=["region_txt", "country_txt", "city", "attacktype1_txt","nkill","iyear"],
                        color_discrete_sequence=["fuchsia"],
                        zoom=1,
            )                       
    fig.update_layout(mapbox_style="open-street-map",
                    autosize=True,
                    margin=dict(l=0, r=0, t=25, b=20),
    )

    return dcc.Graph(figure = fig, style={'height' : '100%'})
