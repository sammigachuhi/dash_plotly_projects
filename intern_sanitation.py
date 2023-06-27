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

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Global sanitation indicators for each country"),

    html.Hr(),

    html.Div([
        # The country dropdown
        dcc.Dropdown(
            options=[{'label': country, 'value': country} for country in df_drinking.Country.unique()],
            # options= df_drinking.Country.unique(),
            value=["Kenya"],
            id="country_dropdown",
            multi=True,
            style= {'width': '70%', 'height': 'auto', 'display': 'inline-block'}
        ),

        # The residence area type dropdown
        dcc.Dropdown(
            options=df_drinking['Residence Area Type'].unique(),
            value='Total',
            id='residence_dropdown',
            style= {'width': '30%', 'display': 'inline-block'}
        )
    ]),

    html.Div(className="row", children=[
        # html.Div(className="six columns", children=[
        #     dcc.Graph("stack_bar_drinking_water")
        # ]),
        html.Div(className="six columns", children=[
            dcc.Graph("line_graph_drinking_water")
        ])
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

# @app.callback(
#     Output("stack_bar_drinking_water", "figure"),
#     Input("country_dropdown", "value"),
# )
# def update_stack_drinking(x_axis_column_name):
#     dff = df_drinking[df_drinking.Country == x_axis_column_name]
#
#     fig = px.bar(dff, x=dff[dff['Country'] == x_axis_column_name['value']],
#                  y='Numeric',
#                  color='Year', barmode='group',
#                  title="Bar graph of drinking water among countries")
#
#     return fig

@app.callback(
    Output("line_graph_drinking_water", "figure"),
    Input("country_dropdown", "value"),
    Input("residence_dropdown", "value")
)
def update_line_drinking(x_axis_column_name, residence_type):
    # if x_axis_column_name == None:
    #     return {}
    # else:
    dff = df_drinking[df_drinking['Country'].isin(x_axis_column_name)] # & df_drinking[df_drinking['Residence Area Type'].isin(residence_type)]
        # dff['Display Value'].astype(int)
        # dff = df_drinking[df_drinking['Residence Area Type'].isin(residence_type)]
    dff = dff.sort_values(by='Year')

    fig = px.line(dff[dff['Residence Area Type'] == residence_type], x='Year', y='Display Value',
                      color='Country', title="Line chart of drinking water")

    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

























