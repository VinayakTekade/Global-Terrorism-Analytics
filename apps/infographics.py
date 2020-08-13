import dash
import dash_html_components as html
import dash_core_components as dcc
from app import app
import dash_bootstrap_components as dbc
import pandas as pd
import calendar
from dash.dependencies import Input, Output, State


from apps import densityGraph
from apps import peopleKilled
from apps import weaponUsed
# from apps import attackType

terrorism = pd.read_csv('apps/data/global_terror_2.csv',
                        encoding='latin-1',
                        low_memory=True, 
                        usecols=['iyear', 'imonth', 'iday', 'country_txt', 'city', 'longitude', 'latitude',
                        'nkill', 'gname','region_txt','provstate', 'attacktype1_txt'])

terrorism = terrorism[terrorism['imonth'] != 0]
terrorism['day_clean'] = [15 if x == 0 else x for x in terrorism['iday']]
terrorism['date'] = [pd.datetime(y, m, d) for y, m, d in zip(terrorism['iyear'], terrorism['imonth'], terrorism['day_clean'])]
terrorism['month_txt'] = pd.DataFrame([calendar.month_name[i] for i in terrorism['imonth']]).astype(str)

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


layout = html.Div([


    navbar,

    html.Div(className='row mx-3', children=[
        html.Div(className='col-3 sidebar', children=[   
                
                dbc.Button(
                        "Intensity of Attacks",
                        color="link",
                        id="group-1-toggle",
                        ),
                dbc.Button(
                        "Comparison of Attack Types",
                        color="link",
                        id="group-2-toggle",
                    ),
                dbc.Button(
                        "People killed per Region",
                        color="link",
                        id="group-3-toggle",
                    ),
                dbc.Button(
                        "Weapon Type Analytics",
                        color="link",
                        id="group-4-toggle",
                    ),
                dbc.Button(
                        "Death Pattern per year",
                        color="link",
                        id="group-5-toggle",
                    ),
                dbc.Button(
                        "Attacks Types used per year",
                        color="link",
                        id="group-6-toggle",
                    ),

        ]),
    
        html.Div(className='col-9 visualisation align-middle', children=[
                dbc.Collapse(
                    html.Div(
                        densityGraph.layout
                    ),
                id="collapse-1",
                ),
                dbc.Collapse(
                    html.Div(
                        # attackType.layout
                    ),
                id="collapse-2",
                ),
                dbc.Collapse(
                    html.Div(
                        peopleKilled.layout
                    ),
                id="collapse-3",
                ),
                dbc.Collapse(
                   html.Div(
                        weaponUsed.layout
                    ),
                id="collapse-4",
                ),
                dbc.Collapse(
                    html.Div([
                        html.H3("Death Pattern per year Clicked")
                    ]),
                id="collapse-5",
                ),
                dbc.Collapse(
                    html.Div([
                        html.H3("Attacks Types used per year Clicked")
                    ]),
                id="collapse-6",
                ),
        ])
    ])
])


@app.callback(
    [Output("collapse-1", "is_open"),Output("collapse-2", "is_open"),Output("collapse-3", "is_open"),Output("collapse-4", "is_open"),Output("collapse-5", "is_open"),Output("collapse-6", "is_open")],
    [Input("group-1-toggle", "n_clicks"),Input("group-2-toggle", "n_clicks"),Input("group-3-toggle", "n_clicks"),Input("group-4-toggle", "n_clicks"),Input("group-5-toggle", "n_clicks"),Input("group-6-toggle", "n_clicks")],
    [State("collapse-1", "is_open"),State("collapse-2", "is_open"),State("collapse-3", "is_open"),State("collapse-4", "is_open"),State("collapse-5", "is_open"),State("collapse-6", "is_open")]
)
def toggle_accordion(n1, n2, n3, n4, n5, n6, is_open1, is_open2, is_open3, is_open4, is_open5, is_open6):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, False, False, False, False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "group-1-toggle" and n1:
        return not is_open1, False, False, False, False, False
    elif button_id == "group-2-toggle" and n2:
        return False, not is_open2, False, False, False, False
    elif button_id == "group-3-toggle" and n3:
        return False, False, not is_open3, False, False, False
    elif button_id == "group-4-toggle" and n4:
        return False, False, False, not is_open4, False, False
    elif button_id == "group-5-toggle" and n5:
        return False, False, False, False, not is_open5, False
    elif button_id == "group-6-toggle" and n6:
        return False, False, False, False, False, not is_open6
    return False, False, False, False, False, False
