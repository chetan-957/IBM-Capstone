# --------------------------------------------------------------
# Hands-on Lab: Build an Interactive Dashboard with Plotly Dash
# --------------------------------------------------------------

# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# --------------------------------------------------------------
# Load Data
# --------------------------------------------------------------

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# --------------------------------------------------------------
# Create Dash App
# --------------------------------------------------------------

app = dash.Dash(__name__)

# --------------------------------------------------------------
# App Layout
# --------------------------------------------------------------

app.layout = html.Div(children=[

    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center',
                   'color': '#503D36',
                   'font-size': 40}),

    # ----------------------------------------------------------
    # TASK 1: Add Dropdown for Launch Site Selection
    # ----------------------------------------------------------

    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # ----------------------------------------------------------
    # TASK 2: Pie Chart for Success Counts
    # ----------------------------------------------------------

    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # ----------------------------------------------------------
    # TASK 3: Add Payload Range Slider
    # ----------------------------------------------------------

    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: '0',
               2500: '2500',
               5000: '5000',
               7500: '7500',
               10000: '10000'},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # ----------------------------------------------------------
    # TASK 4: Scatter Chart for Payload vs Success
    # ----------------------------------------------------------

    html.Div(dcc.Graph(id='success-payload-scatter-chart'))

])

# --------------------------------------------------------------
# TASK 2: Callback for Pie Chart
# --------------------------------------------------------------

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):

    if selected_site == 'ALL':
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failure for {selected_site}'
        )

    return fig


# --------------------------------------------------------------
# TASK 4: Callback for Scatter Plot
# --------------------------------------------------------------

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter_chart(selected_site, payload_range):

    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs Launch Outcome (All Sites)'
        )
    else:
        filtered_df = filtered_df[
            filtered_df['Launch Site'] == selected_site
        ]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs Launch Outcome ({selected_site})'
        )

    return fig


# --------------------------------------------------------------
# Run App
# --------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
