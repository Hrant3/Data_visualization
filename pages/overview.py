import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

dash.register_page(__name__, path='/')

# Load and prepare the data
df = pd.read_csv('MARKET_Car_Prices.csv')

# Convert cylinder names to numbers
cylinder_map = {'two': 2, 'four': 4, 'six': 6, 'eight': 8, 'three': 3, 'twelve': 12, 'five': 5}
df['num_of_cylinders'] = df['num_of_cylinders'].map(cylinder_map)

# Create the layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Car Market Overview", className="text-primary mb-4"),
            html.P("Explore the car market data through interactive visualizations.", className="lead")
        ])
    ]),
    
    # New Price Distribution Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Overall Price Distribution"),
                dbc.CardBody([
                    html.P("The distribution of car prices shows the concentration of vehicles across different price ranges.", 
                           className="text-muted"),
                    dcc.Graph(id='price-histogram'),
                    dcc.RangeSlider(
                        id='price-bins-slider',
                        min=10,
                        max=100,
                        step=5,
                        value=[50],
                        marks={i: str(i) for i in range(10, 101, 10)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Small("Adjust the slider to change the number of bins in the histogram", 
                             className="text-muted mt-2")
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Price Distribution by Manufacturer"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='make-selector',
                        options=[{'label': make, 'value': make} for make in sorted(df['make'].unique())],
                        value=df['make'].unique()[:5].tolist(),
                        multi=True
                    ),
                    dcc.Graph(id='price-distribution-plot')
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Price vs. Fuel Efficiency"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='mpg-type',
                        options=[
                            {'label': 'City MPG', 'value': 'city_mpg'},
                            {'label': 'Highway MPG', 'value': 'highway_mpg'}
                        ],
                        value='city_mpg',
                        clearable=False
                    ),
                    dcc.Graph(id='mpg-price-scatter'),
                    dcc.RangeSlider(
                        id='mpg-range',
                        min=df['city_mpg'].min(),
                        max=df['city_mpg'].max(),
                        value=[df['city_mpg'].min(), df['city_mpg'].max()],
                        marks={int(i): f'{int(i)} MPG' for i in 
                               [df['city_mpg'].min(), df['city_mpg'].max()/2, df['city_mpg'].max()]}
                    )
                ])
            ])
        ], width=12)
    ])
])

@callback(
    Output('price-histogram', 'figure'),
    Input('price-bins-slider', 'value')
)
def update_price_histogram(nbins):
    fig = px.histogram(df, x='price', nbins=nbins[0],
                      title='Distribution of Car Prices',
                      labels={'price': 'Price (USD)', 'count': 'Number of Cars'})
    
    fig.update_layout(
        showlegend=False,
        xaxis_title='Price (USD)',
        yaxis_title='Number of Cars',
        bargap=0.1
    )
    
    # Add insights annotation
    fig.add_annotation(
        text="Most cars are clustered at the lower end of the price range,<br>with fewer models in higher price segments.",
        xref="paper", yref="paper",
        x=0.98, y=0.98,
        showarrow=False,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="rgba(0, 0, 0, 0.2)",
        borderwidth=1,
        borderpad=4,
        align="right"
    )
    
    return fig

@callback(
    Output('price-distribution-plot', 'figure'),
    Input('make-selector', 'value')
)
def update_price_distribution(selected_makes):
    if not selected_makes:
        selected_makes = df['make'].unique()[:5].tolist()
    
    filtered_df = df[df['make'].isin(selected_makes)]
    fig = px.box(filtered_df, x='make', y='price', 
                 title='Price Distribution by Manufacturer',
                 color='make')
    fig.update_layout(showlegend=False)
    return fig

@callback(
    [Output('mpg-price-scatter', 'figure'),
     Output('mpg-range', 'min'),
     Output('mpg-range', 'max'),
     Output('mpg-range', 'value'),
     Output('mpg-range', 'marks')],
    [Input('mpg-type', 'value'),
     Input('mpg-range', 'value')]
)
def update_scatter_plot(mpg_type, mpg_range):
    if mpg_range is None:
        mpg_range = [df[mpg_type].min(), df[mpg_type].max()]
    
    filtered_df = df[(df[mpg_type] >= mpg_range[0]) & 
                    (df[mpg_type] <= mpg_range[1])]
    
    fig = px.scatter(filtered_df, x=mpg_type, y='price',
                     color='num_of_cylinders',
                     hover_data=['make', 'body_style', 'engine_type', mpg_type],
                     title=f'Price vs. {"City" if mpg_type == "city_mpg" else "Highway"} MPG')
    
    # Update range slider properties based on selected MPG type
    min_val = df[mpg_type].min()
    max_val = df[mpg_type].max()
    marks = {int(i): f'{int(i)} MPG' for i in 
            [min_val, (min_val + max_val)/2, max_val]}
    
    return fig, min_val, max_val, [min_val, max_val], marks 