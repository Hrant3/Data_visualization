import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd

# Initialize the Dash app with a modern theme
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.FLATLY],
                use_pages=True)

# Load the data
df = pd.read_csv('MARKET_Car_Prices.csv')

# Create the logo
logo = html.Div([
    html.Div(className="car-logo"),
    html.Span("CarMarket", className="logo-text")
], className="logo-container")

# Create the layout
app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Overview", href="/")),
            dbc.NavItem(dbc.NavLink("Detailed Analysis", href="/analysis")),
        ],
        brand=logo,
        brand_href="/",
        color="primary",
        dark=True,
        className="custom-navbar"
    ),
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8051) 