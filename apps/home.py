import dash
import dash_html_components as html
from app import app
import dash_bootstrap_components as dbc

def navbar_ui_dark():
    navbar_dark = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="#"), className='selected'),
            dbc.NavItem(dbc.NavLink("Map", href="/map")),
            dbc.NavItem(dbc.NavLink("Chart", href="/chart")),
            dbc.NavItem(dbc.NavLink("Infographics", href="/infographics")),
        ],
        brand="Global Terrorism Analytics",
        brand_href="#",
        color='transparent',
        dark=True,
        className="navbar-home",
        fluid=True
    )
    
    return navbar_dark

layout = html.Div([
    navbar_ui_dark(),
], className="home")
