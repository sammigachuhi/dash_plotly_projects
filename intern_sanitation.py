from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np

# Import the data
df_drinking = pd.read_csv("archive/Basic and safely managed drinking water services.csv")
df_sanitation = pd.read_csv("archive/Basic and safely managed sanitation services.csv")
df_handwashing = pd.read_csv("archive/Handwashing with soap.csv")
df_defecation = pd.read_csv("archive/Open defecation.csv")

# External stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Map countries to color
c = dict(zip(df_drinking.Country.unique(), px.colors.qualitative.Plotly))

# Create the app layout
app.layout = html.Div([
    html.H1("Global sanitation indicators for each country"),

    html.Hr(),

    # Indicate reason for zigzag lines
    dcc.Markdown('''
    *Some indicators could have duplicate values, thus the reason for some line graphs appearing in a zigzag format* 
    
    *This is especially for `Total` and `Urban` variables*
    '''),

    html.Hr(),

    html.Div(className="row", children=[
        # The country dropdown
        dcc.Dropdown(className="six columns",
            options=[{'label': country, 'value': country} for country in df_drinking.Country.unique()],
            # options= df_drinking.Country.unique(),
            value=["Kenya"],
            id="country_dropdown",
            multi=True,
            style= {'width': '70%', 'height': 'auto', 'display': 'inline-block'}
        ),

        # The residence area type dropdown
        dcc.Dropdown(className="six columns",
            options=df_drinking['Residence Area Type'].unique(),
            value='Total',
            id='residence_dropdown',
            style= {'width': '30%', 'display': 'inline-block'}
        )
    ]),

    html.Br(),
    html.Br(),

    # Drinking water
    html.Div(className="row", children=[
        html.Div(className="six columns", children=[
            dcc.Graph(id="stack_bar_drinking_water", style={"display": "inline-block"})
        ]),
        html.Div(className="six columns", children=[
            dcc.Graph(id="line_graph_drinking_water", style={"display": "inline-block"})
        ]),
    ]),

    # Download button for drinking water dataframe
    html.Div(children=[
        html.Div(children=[
            html.Button("Download Drinking Water Dataframe", id="drinking_water_df"),
            dcc.Download(id="download_drinking_water_csv")
        ])
    ]),

    # Sanitation services
    html.Div(className="row", children=[
        html.Div(className="six columns", children=[
            dcc.Graph("stack_bar_sanitation_services")
        ]),
        html.Div(className="six columns", children=[
            dcc.Graph("line_graph_sanitation_services")
        ])
    ]),

    # Download button for sanitation services dataframe
    html.Div(children=[
        html.Div(children=[
            html.Button("Download Sanitation Services Dataframe", id="sanitation_services_df"),
            dcc.Download(id="download_sanitation_services_csv")
        ])
    ]),

    # Handwashing
    html.Div(className="row", children=[
        html.Div(className="six columns", children=[
            dcc.Graph("stack_bar_handwashing")
        ]),
        html.Div(className="six columns", children=[
            dcc.Graph("line_graph_handwashing")
        ])
    ]),

    # Download button for handwashing dataframe
    html.Div(children=[
        html.Div(children=[
            html.Button("Download Handwashing Dataframe", id="handwashing_df"),
            dcc.Download(id="download_handwashing_csv")
        ])
    ]),

    # Open defecation
    html.Div(className="row", children=[
        html.Div(className="six columns", children=[
            dcc.Graph("stack_bar_defecation")
        ]),
        html.Div(className="six columns", children=[
            dcc.Graph("line_graph_defecation")
        ])
    ]),

    # Download button for open defecation dataframe
    html.Div(children=[
        html.Div(children=[
            html.Button("Download Open Defecation Dataframe", id="open_defecation_df"),
            dcc.Download(id="download_open_defecation_csv")
        ])
    ]),

])

# Bar chart for drinking water
@app.callback(
    Output("stack_bar_drinking_water", "figure"),
    Input("country_dropdown", "value"),
    Input("residence_dropdown", "value")
)
def histogram(x_axis_column_name, residence_type):
    dff = df_drinking[df_drinking['Country'].isin(x_axis_column_name)]
    dff = dff.sort_values(by='Year')

    fig = px.histogram(dff[dff['Residence Area Type'] == residence_type], x='Country', y='Display Value', histfunc='avg',
                       color='Country', title=f"Bar chart showing average percentage (%) of population using safely " + "<br>" +
                                              f"managed drinking-water services (%) {dff['Year'].min()}-{dff['Year'].max()}",
                       color_discrete_map=c,
                       )

    fig.update_layout(transition={'duration': 100,
                                  'easing': 'linear'})

    return fig

# Line chart for drinking
@app.callback(
    Output("line_graph_drinking_water", "figure"),
    Input("country_dropdown", "value"),
    Input("residence_dropdown", "value")
)
def line_chart(x_axis_column_name, residence_type):

    dff = df_drinking[df_drinking['Country'].isin(x_axis_column_name)]
    dff = dff.sort_values(by='Year')

    fig = px.line(dff[dff['Residence Area Type'] == residence_type], x='Year', y='Display Value', markers=True,
                      color='Country', title=f"Line chart showing population using safely " + "<br>" +
                                             f"managed drinking-water services (%) {dff['Year'].min()}-{dff['Year'].max()}",
                  color_discrete_map=c,
                  )

    fig.update_layout(transition={'duration': 100,
                                  'easing': 'linear'})

    return fig

# Function to download drinking water dataframe
@app.callback(
    Output("download_drinking_water_csv", "data"),
    Input("drinking_water_df", "n_clicks"),
    prevent_initial_call=True
)
def download_df(n_clicks):
    return dcc.send_data_frame(df_drinking.to_csv, "drinking_water.csv")

# Bar chart for sanitation services
@app.callback(
    Output("stack_bar_sanitation_services", "figure"),
    Input("country_dropdown", "value"),
    Input("residence_dropdown", "value")
)
def histogram(x_axis_column_name, residence_type):
    dff = df_sanitation[df_sanitation['Country'].isin(x_axis_column_name)]
    dff = dff.sort_values(by='Year')

    fig = px.histogram(dff[dff['Residence Area Type'] == residence_type], x='Country', y='Display Value',
                       histfunc='avg',
                       color='Country', title=f"Bar chart showing average percentage (%) of population using safely " + "<br>" +
                                              f"managed sanitation services {dff['Year'].min()}-{dff['Year'].max()}",
                       color_discrete_map=c,
                       )

    fig.update_layout(transition={'duration': 100,
                                  'easing': 'linear'})

    return fig

# Line Graph for sanitation services
@app.callback(
    Output("line_graph_sanitation_services", "figure"),
    Input("country_dropdown", "value"),
    Input("residence_dropdown", "value")
)
def line_chart(x_axis_column_name, residence_type):

    dff = df_sanitation[df_sanitation['Country'].isin(x_axis_column_name)]
    dff = dff.sort_values(by='Year')

    fig = px.line(dff[dff['Residence Area Type'] == residence_type], x='Year', y='Display Value', markers=True,
                      color='Country', title=f"Line chart showing population using safely " + "<br>" +
                                             f"safely managed sanitation services (%) {dff['Year'].min()}-{dff['Year'].max()}",
                  color_discrete_map=c,
                 )

    fig.update_layout(transition={'duration': 100,
                                  'easing': 'linear'})

    return fig

# Function to download sanitation services dataframe
@app.callback(
    Output("download_sanitation_services_csv", "data"),
    Input("sanitation_services_df", "n_clicks"),
    prevent_initial_call=True
)
def download_df(n_clicks):
    return dcc.send_data_frame(df_sanitation.to_csv, "sanitation_services.csv")

# Bar chart for handwashing services
@app.callback(
    Output("stack_bar_handwashing", "figure"),
    Input("country_dropdown", "value"),
    Input("residence_dropdown", "value")
)
def histogram(x_axis_column_name, residence_type):
    dff = df_handwashing[df_handwashing['Country'].isin(x_axis_column_name)]
    dff = dff.sort_values(by='Year')

    fig = px.histogram(dff[dff['Residence Area Type'] == residence_type], x='Country', y='Display Value',
                       histfunc='avg',
                       color='Country', title=f"Bar chart showing average percentage (%) of population using " + "<br>" +
                                              f"basic handwashing facilities at home {dff['Year'].min()}-{dff['Year'].max()}",
                       color_discrete_map=c,
                       )

    fig.update_layout(transition={'duration': 100,
                                  'easing': 'linear'})

    return fig

# Line chart for handwashing
@app.callback(
    Output("line_graph_handwashing", "figure"),
    Input("country_dropdown", "value"),
    Input("residence_dropdown", "value")
)
def line_chart(x_axis_column_name, residence_type):

    dff = df_handwashing[df_handwashing['Country'].isin(x_axis_column_name)]
    dff = dff.sort_values(by='Year')

    fig = px.line(dff[dff['Residence Area Type'] == residence_type], x='Year', y='Display Value', markers=True,
                      color='Country', title=f"Line chart showing population using " + "<br>" +
                                             f"basic handwashing facilities at home (%) {dff['Year'].min()}-{dff['Year'].max()}",
                  color_discrete_map=c,
                  )

    fig.update_layout(transition={'duration': 100,
                                  'easing': 'linear'})

    return fig

# Function to download handwashing dataframe
@app.callback(
    Output("download_handwashing_csv", "data"),
    Input("handwashing_df", "n_clicks"),
    prevent_initial_call=True
)
def download_df(n_clicks):
    return dcc.send_data_frame(df_handwashing.to_csv, "handwashing.csv")

# Bar chart for open defecation
@app.callback(
    Output("stack_bar_defecation", "figure"),
    Input("country_dropdown", "value"),
    Input("residence_dropdown", "value")
)
def histogram(x_axis_column_name, residence_type):
    dff = df_defecation[df_defecation['Country'].isin(x_axis_column_name)]
    dff = dff.sort_values(by='Year')

    fig = px.histogram(dff[dff['Residence Area Type'] == residence_type], x='Country', y='Display Value',
                       histfunc='avg',
                       color='Country', title=f"Bar chart showing average percentage of " + "<br>" +
                                              f"population practising open defecation (% Average) {dff['Year'].min()}-{dff['Year'].max()}",
                       color_discrete_map=c,
                       )

    fig.update_layout(transition={'duration': 100,
                                  'easing': 'linear'})

    return fig

# Line chart for open defecation
@app.callback(
    Output("line_graph_defecation", "figure"),
    Input("country_dropdown", "value"),
    Input("residence_dropdown", "value")
)
def line_chart(x_axis_column_name, residence_type):

    dff = df_defecation[df_defecation['Country'].isin(x_axis_column_name)]
    dff = dff.sort_values(by='Year')

    fig = px.line(dff[dff['Residence Area Type'] == residence_type], x='Year', y='Display Value', markers=True,
                      color='Country', title=f"Line chart showing population practising open defecation (%) {dff['Year'].min()}-{dff['Year'].max()}",
                  color_discrete_map=c,
                  )

    fig.update_layout(transition={'duration': 100,
                                  'easing': 'linear'})

    return fig

# Function to download open defecation dataframe
@app.callback(
    Output("download_open_defecation_csv", "data"),
    Input("open_defecation_df", "n_clicks"),
    prevent_initial_call=True
)
def download_df(n_clicks):
    return dcc.send_data_frame(df_defecation.to_csv, "open_defecation.csv")

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

























