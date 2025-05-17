import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

dash.register_page(__name__, path='/analysis')

# Load and prepare the data
df = pd.read_csv('MARKET_Car_Prices.csv')
cylinder_map = {'two': 2, 'four': 4, 'six': 6, 'eight': 8, 'three': 3, 'twelve': 12, 'five': 5}
df['num_of_cylinders'] = df['num_of_cylinders'].map(cylinder_map)

# Create the layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Detailed Market Analysis", className="text-primary mb-4"),
            html.P("Explore detailed relationships between various car features.", className="lead")
        ])
    ]),
    
    # Price vs Performance Metrics
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Price vs Performance Metrics"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='performance-metric',
                        options=[
                            {'label': 'Horsepower', 'value': 'horsepower'},
                            {'label': 'Engine Size', 'value': 'engine_size'},
                            {'label': 'Peak RPM', 'value': 'peak_rpm'},
                            {'label': 'Curb Weight', 'value': 'curb_weight'}
                        ],
                        value='horsepower',
                        clearable=False
                    ),
                    dcc.Graph(id='performance-scatter')
                ])
            ])
        ], width=12, className="mb-4")
    ]),
    
    # Car Features Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Price Distribution by Car Features"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='feature-selector',
                        options=[
                            {'label': 'Body Style', 'value': 'body_style'},
                            {'label': 'Number of Cylinders', 'value': 'num_of_cylinders'},
                            {'label': 'Fuel Type', 'value': 'fuel_type'},
                            {'label': 'Drive Wheels', 'value': 'drive_wheels'},
                            {'label': 'Aspiration', 'value': 'aspiration'}
                        ],
                        value='body_style',
                        clearable=False
                    ),
                    dcc.Graph(id='feature-box')
                ])
            ])
        ], width=12, className="mb-4")
    ]),
    
    # Market Segment Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Market Segment Analysis"),
                dbc.CardBody([
                    dcc.Graph(id='segment-analysis'),
                    dcc.RangeSlider(
                        id='price-range',
                        min=df['price'].min(),
                        max=df['price'].max(),
                        value=[df['price'].min(), df['price'].max()],
                        marks={int(i): f'${int(i):,}' for i in 
                               np.linspace(df['price'].min(), df['price'].max(), 5)}
                    )
                ])
            ])
        ], width=12)
    ])
])

@callback(
    Output('performance-scatter', 'figure'),
    Input('performance-metric', 'value')
)
def update_performance_scatter(metric):
    fig = px.scatter(df, x=metric, y='price',
                    color='num_of_cylinders',
                    title=f'Price vs {metric.replace("_", " ").title()}',
                    labels={metric: metric.replace("_", " ").title(),
                           'price': 'Price (USD)',
                           'num_of_cylinders': 'Number of Cylinders'})
    
    fig.update_layout(
        showlegend=True,
        height=500
    )
    return fig

@callback(
    Output('feature-box', 'figure'),
    Input('feature-selector', 'value')
)
def update_feature_box(feature):
    fig = px.box(df, x=feature, y='price',
                 title=f'Price Distribution by {feature.replace("_", " ").title()}',
                 labels={feature: feature.replace("_", " ").title(),
                        'price': 'Price (USD)'})
    
    fig.update_layout(
        showlegend=False,
        height=500,
        xaxis_tickangle=-45
    )
    return fig

@callback(
    Output('segment-analysis', 'figure'),
    Input('price-range', 'value')
)
def update_segment_analysis(price_range):
    filtered_df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]
    
    # Create segments based on price
    filtered_df['price_segment'] = pd.qcut(filtered_df['price'], q=3, 
                                         labels=['Budget', 'Mid-range', 'Luxury'])
    
    segment_stats = filtered_df.groupby('price_segment').agg({
        'num_of_cylinders': 'mean',
        'city_mpg': 'mean',
        'highway_mpg': 'mean',
        'horsepower': 'mean',
        'engine_size': 'mean',
        'price': 'count'
    }).reset_index()
    
    fig = go.Figure(data=[
        go.Bar(name='Avg Cylinders', y=segment_stats['price_segment'], 
               x=segment_stats['num_of_cylinders'], orientation='h'),
        go.Bar(name='Avg City MPG', y=segment_stats['price_segment'], 
               x=segment_stats['city_mpg'], orientation='h'),
        go.Bar(name='Avg Highway MPG', y=segment_stats['price_segment'], 
               x=segment_stats['highway_mpg'], orientation='h'),
        go.Bar(name='Avg Horsepower', y=segment_stats['price_segment'], 
               x=segment_stats['horsepower'], orientation='h'),
        go.Bar(name='Avg Engine Size', y=segment_stats['price_segment'], 
               x=segment_stats['engine_size'], orientation='h')
    ])
    
    fig.update_layout(
        title='Market Segment Analysis',
        barmode='group',
        height=400,
        xaxis_title='Value',
        yaxis_title='Price Segment'
    )
    return fig 