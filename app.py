import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# Read CSV
df = pd.read_csv("data/daily_sales_data_0.csv")
df['date'] = pd.to_datetime(df['date'])
df['sales'] = df['price'] * df['quantity']

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Quantium Forage Dashboard"

# Layout
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'margin': '20px'}, children=[

    # Header
    html.H1("Quantium Forage Dashboard", style={'textAlign': 'center', 'color': '#003366'}),

    # Filters
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'margin': '20px 0'}, children=[
        html.Div([
            html.Label("Select Product:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='product-dropdown',
                options=[{'label': x, 'value': x} for x in df['product'].unique()],
                value=df['product'].unique()[0],
                clearable=False
            ),
        ], style={'width': '48%'}),
        html.Div([
            html.Label("Select Region:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': 'All', 'value': 'All'}] +
                        [{'label': x, 'value': x} for x in df['region'].unique()],
                value='All',
                clearable=False
            ),
        ], style={'width': '48%'})
    ]),

    # Summary cards
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'margin': '20px 0'}, children=[
        html.Div(id='total-sales', style={'flex': 1, 'marginRight': '10px', 'padding': '20px',
                                          'backgroundColor': '#cce5ff', 'borderRadius': '10px',
                                          'textAlign': 'center', 'boxShadow': '2px 2px 10px #888888'}),
        html.Div(id='avg-sales', style={'flex': 1, 'marginLeft': '10px', 'padding': '20px',
                                        'backgroundColor': '#d4edda', 'borderRadius': '10px',
                                        'textAlign': 'center', 'boxShadow': '2px 2px 10px #888888'})
    ]),

    # Graphs
    html.Div([
        dcc.Graph(id='sales-graph', style={'marginBottom': '40px'}),
        dcc.Graph(id='region-sales-graph')
    ])
])

# Callback for line chart & summary cards
@app.callback(
    [Output('sales-graph', 'figure'),
     Output('total-sales', 'children'),
     Output('avg-sales', 'children')],
    [Input('product-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_graphs(selected_product, selected_region):
    filtered_df = df[df['product'] == selected_product]
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]

    # Line chart
    fig_line = {
        'data': [{
            'x': filtered_df['date'],
            'y': filtered_df['sales'],
            'type': 'line',
            'marker': {'color': '#003366'},
            'name': selected_product
        }],
        'layout': {
            'title': f"{selected_product} Sales Over Time",
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Sales'},
            'plot_bgcolor': '#f9f9f9',
            'paper_bgcolor': '#f9f9f9',
            'font': {'color': '#003366'}
        }
    }

    # Summary cards
    total_sales = filtered_df['sales'].sum()
    avg_sales = filtered_df.groupby('date')['sales'].sum().mean()

    total_sales_text = html.Div([
        html.H4("Total Sales", style={'color': '#003366'}),
        html.H2(f"${total_sales:,.2f}", style={'color': '#003366'})
    ])

    avg_sales_text = html.Div([
        html.H4("Average Sales per Day", style={'color': '#155724'}),
        html.H2(f"${avg_sales:,.2f}", style={'color': '#155724'})
    ])

    return fig_line, total_sales_text, avg_sales_text

# Callback for bar chart
@app.callback(
    Output('region-sales-graph', 'figure'),
    [Input('product-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_region_sales(selected_product, selected_region):
    filtered_df = df[df['product'] == selected_product]
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]

    region_sales = filtered_df.groupby('region')['sales'].sum().reset_index()

    fig_bar = {
        'data': [{
            'x': region_sales['region'],
            'y': region_sales['sales'],
            'type': 'bar',
            'marker': {'color': '#28a745'},
            'name': selected_product
        }],
        'layout': {
            'title': f"Total Sales of {selected_product} by Region",
            'xaxis': {'title': 'Region'},
            'yaxis': {'title': 'Total Sales'},
            'plot_bgcolor': '#f9f9f9',
            'paper_bgcolor': '#f9f9f9',
            'font': {'color': '#003366'}
        }
    }
    return fig_bar

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
