# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
# Get unique launch site names for the dropdown
launch_sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'}
                                    ] + [{'label': site, 'value': site} for site in launch_sites],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, 
                                    max=10000, 
                                    step=1000,
                                    marks={i: '{} Kg'.format(i) for i in range(0, 10001, 2500)},  # Custom marks at 0, 2500, 5000, 7500, 10000
                                    value=[min_payload, max_payload]
                                ),
                                
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df

    if entered_site == 'ALL':
        # Calculate total success and failure counts for all sites
        fig = px.pie(
            data_frame=filtered_df, 
            names='class', 
            title='Total Success and Failure Launches for All Sites',
            hole=0.3,
            color_discrete_sequence=['red', 'green'],
        )
        fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
        return fig

    else:
        # Filter dataframe by selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Generate pie chart for the selected site
        fig = px.pie(
            data_frame=filtered_df, 
            names='class', 
            title=f'Success and Failure Launches for {entered_site}',
            hole=0.3,
            color_discrete_sequence=['red', 'green'],
        )
        fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]

    if entered_site == 'ALL':
        # If all sites are selected, plot all data with payload mass and class
        fig = px.scatter(
            filtered_df, x='Payload Mass (kg)', y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for All Sites',
            labels={'class': 'Launch Outcome'},
            hover_data=['Launch Site']
        )
        return fig
    else:
        # Filter dataframe by selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        # Generate scatter plot for the selected site
        fig = px.scatter(
            filtered_df, x='Payload Mass (kg)', y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for {entered_site}',
            labels={'class': 'Launch Outcome'},
            hover_data=['Launch Site']
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
