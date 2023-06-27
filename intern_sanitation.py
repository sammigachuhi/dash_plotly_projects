from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np

# Import the data
df_drinking = pd.read_csv("archive/Basic and safely managed drinking water services.csv")
# df_drinking = df_drinking[df_drinking['Residence Area Type'] == 'Total']
df_sanitation = pd.read_csv("archive/Basic and safely managed drinking water services.csv")
df_handwashing = pd.read_csv("archive/Basic and safely managed drinking water services.csv")
df_defecation = pd.read_csv("archive/Open defecation.csv")

# External stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Map countries to color
# map emotions to a color
c = dict(zip(df_drinking.Country.unique(), px.colors.qualitative.G10))

app.layout = html.Div([
    html.H1("Global sanitation indicators for each country"),

    html.Hr(),
    # Indicate reason for zigzag lines
    html.H6("Some indicators could have duplicate values, thus the reason for some line graphs appearing in a zigzag format"),

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

    html.Div(className="row", children=[
        html.Div(className="six columns", children=[
            dcc.Graph(id="stack_bar_drinking_water", style={"display": "inline-block"})
        ]),
        html.Div(className="six columns", children=[
            dcc.Graph(id="line_graph_drinking_water", style={"display": "inline-block"})
        ]),
    ]),

    # html.Div(className="row", children=[
    #     html.Div(className="six columns", children=[
    #         dcc.Graph("stack_bar_sanitation_services")
    #     ]),
    #     html.Div(className="six columns", children=[
    #         dcc.Graph("line_graph_sanitation_services")
    #     ])
    # ]),

    # html.Div(className="row", children=[
    #     html.Div(className="six columns", children=[
    #         dcc.Graph("stack_bar_handwashing")
    #     ]),
    #     html.Div(className="six columns", children=[
    #         dcc.Graph("line_graph_handwashing")
    #     ])
    # ]),

    # html.Div(className="row", children=[
    #     html.Div(className="six columns", children=[
    #         dcc.Graph("stack_bar_defecation")
    #     ]),
    #     html.Div(className="six columns", children=[
    #         dcc.Graph("line_graph_defecation")
    #     ])
    # ])
])

@app.callback(
    Output("stack_bar_drinking_water", "figure"),
    Input("country_dropdown", "value"),
    Input("residence_dropdown", "value")
)
def update_stack_drinking(x_axis_column_name, residence_type):
    dff = df_drinking[df_drinking.Country.isin(x_axis_column_name)]

    fig = px.histogram(dff[dff['Residence Area Type'] == residence_type], x='Country', y='Display Value', histfunc='avg',
                       color='Country', title="Bar Chart Showing Population using safely \n"
                                              " managed drinking-water services (%)",
                       color_discrete_map=c)

    return fig

@app.callback(
    Output("line_graph_drinking_water", "figure"),
    Input("country_dropdown", "value"),
    Input("residence_dropdown", "value")
)
def update_line_drinking(x_axis_column_name, residence_type):

    dff = df_drinking[df_drinking['Country'].isin(x_axis_column_name)]
    dff = dff.sort_values(by='Year')

    fig = px.line(dff[dff['Residence Area Type'] == residence_type], x='Year', y='Display Value', markers=True,
                      color='Country', title="Line Chart Showing Population using safely \n"
                                             "managed drinking-water services (%)",
                  color_discrete_map=c)

    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

























