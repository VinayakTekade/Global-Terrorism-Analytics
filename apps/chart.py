import dash
import dash_html_components as html
from app import app
import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Map", href="/map")),
        dbc.NavItem(dbc.NavLink("Chart", href="#")),
        dbc.NavItem(dbc.NavLink("Infographics", href="/infographics")),
    ],
    brand="Global Terrorism Data Visualization",
    brand_href="#",
    color="light",
    dark=False,
)

layout = html.Div([
    navbar,
    html.Div(className='container', children=[
            html.H3('Chart page')
        ])
])