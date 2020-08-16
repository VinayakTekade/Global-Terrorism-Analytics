import dash
import dash_html_components as html
from app import app
import dash_bootstrap_components as dbc

def navbar_ui():
    """
    Displays navbar
    """
    navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Map", href="/map")),
        dbc.NavItem(dbc.NavLink("Chart", href="/chart")),
        dbc.NavItem(dbc.NavLink("Infographics", href="#"), className='selected')
    ],
    brand="Global Terrorism Analytics",
    brand_href="#",
    color="light",
    dark=False,
    className="navbar",
    fluid=True
    )
    return navbar

def pattern_selector():
    """
    Displays pattern options available
    """
    
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
    return nav


layout = html.Div([


    navbar_ui(),

    html.Div(className='row mx-3', children=[
        html.Div(className='col-3 sidebar', children=[   
                pattern_selector()
        ]),
    
        html.Div(className='col-9 visualisation align-middle', children=[
               html.H3("Select an option from sidebar")
        ])
    ])
])

