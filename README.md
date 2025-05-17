# Car Market Analysis Dashboard

An interactive dashboard built with Dash and Plotly to analyze car market data.

## Features

- Interactive visualizations of car market data
- Multiple pages with different analysis perspectives
- Responsive design for various screen sizes
- Interactive components (dropdowns, sliders, etc.)
- Clean and modern UI

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:8050`

## Pages

1. **Overview**
   - Price distribution by brand
   - Price vs. Mileage analysis with interactive filters

2. **Detailed Analysis**
   - Feature correlation analysis
   - Price trends by year
   - Market segment analysis

## Interactive Components

- Brand selector dropdown
- Mileage range slider
- Feature correlation selector
- Price range filter
- Trend type selector (mean/median)

## Data Source

The dashboard uses the MARKET_Car_Prices.csv dataset, which contains information about various car models, including:
- Brand and model
- Price
- Mileage
- Number of cylinders
- Year of manufacture