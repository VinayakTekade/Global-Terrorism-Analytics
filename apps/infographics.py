import dash
import dash_html_components as html
import dash_core_components as dcc
from app import app
import dash_bootstrap_components as dbc
import pandas as pd
import calendar
from dash.dependencies import Input, Output, State

terrorism = pd.read_csv('apps/data/global_terror.csv',
                        encoding='latin-1',
                        low_memory=True, 
                        usecols=['iyear', 'imonth', 'iday', 'country_txt', 'city', 'longitude', 'latitude',
                        'nkill', 'nwound', 'summary', 'target1', 'gname','region_txt','provstate', 'attacktype1_txt'])

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

accordian1 = html.Div(
        [

                html.Div(
                    [
                        dbc.Button(
                        "Intensity of Attacks",
                        color="link",
                        id="group-1-toggle",
                        ),
                        dbc.Button(
                        "Start",
                        color="primary",
                        )
                    ], className="d-flex justify-content-between pr-5"
                ),
            dbc.Collapse(
                # html.Div([
                #     dbc.Button(
                #         "Start",
                #         color="primary",
                #     )
                # ]),
                id="collapse-1",
            ),
        ]
    )

accordian2 = html.Div(
        [
                html.H2(
                    dbc.Button(
                        "Comparison of Attack Types",
                        color="link",
                        id="group-2-toggle",
                    )
                ),
            dbc.Collapse(
                    html.Div([
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
                         html.Div([
                            dbc.Button(
                                "Start",
                                color="primary",
                                block="true"
                            )
                        ], className="dropdown")
                    ]),
                    id="collapse-2", className="accordian-space"
            ),
        ]
    )

accordian3 = html.Div(
        [

                html.H2(
                    dbc.Button(
                        "People killed per Region",
                        color="link",
                        id="group-3-toggle",
                    )
                ),
            dbc.Collapse(
                    html.Div([
                       # countries
                        html.Div([
                            dcc.Dropdown(id='countries', className='dropdown',
                                        multi=True,
                                        value=[''],
                                        placeholder='Select Countries',
                                        options=[{'label': c, 'value': c}
                                                for c in sorted(terrorism['country_txt'].unique())])
                        ]),
                        html.Div([
                            dbc.Button(
                                "Start",
                                color="primary",
                                block="true"
                            )
                        ], className="dropdown")
                    ]),
                    id="collapse-3", className="accordian-space"
            ),
        ]
    )

accordian4 = html.Div(
        [

                html.H2(
                    dbc.Button(
                        "Weapon Type Analytics",
                        color="link",
                        id="group-4-toggle",
                    )
                ),
            dbc.Collapse(
                    html.Div([
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
                        html.Div([
                            dbc.Button(
                                "Start",
                                color="primary",
                                block="true"
                            )
                        ], className="dropdown")
                    ]),
                    id="collapse-4", className="accordian-space"
            ),
        ]
    )

accordian5 = html.Div(
        [

                html.H2(
                    dbc.Button(
                        "Death Pattern per year",
                        color="link",
                        id="group-5-toggle",
                    )
                ),
            dbc.Collapse(
                    html.Div([
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
                        html.Div([
                            dbc.Button(
                                "Start",
                                color="primary",
                                block="true"
                            )
                        ], className="dropdown")
                    ]),
                    id="collapse-5", className="accordian-space"
            ),
        ]
    )

accordian6 = html.Div(
        [
             
                html.H2(
                    dbc.Button(
                        "Attacks Types used per year",
                        color="link",
                        id="group-6-toggle",
                    )
                ),
            dbc.Collapse(
                    html.Div([
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
                        html.Div([
                            dbc.Button(
                                "Start",
                                color="primary",
                                block="true"
                            )
                        ], className="dropdown")
                    ]),
                    id="collapse-6", className="accordian-space"
            ),
        ]
    )



accordion = html.Div(
    [
        accordian1,
        accordian2,
        accordian3,
        accordian4,
        accordian5,
        accordian6,
    ], className="accordion"
)





layout = html.Div([


    navbar,

    html.Div(className='row mx-3', children=[
        html.Div(className='col-3 sidebar', children=[   
                accordion
        ]),
    
        html.Div(className='col-9 visualisation align-middle', children=[
           
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
