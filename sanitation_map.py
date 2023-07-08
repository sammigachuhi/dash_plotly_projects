import plotly.express as px
import pandas as pd
from dash import Dash, dcc, Input, Output, html

df_drinking = pd.read_csv("archive/Basic and safely managed drinking water services.csv")
df_sanitation = pd.read_csv("archive/Basic and safely managed sanitation services.csv")
df_handwashing = pd.read_csv("archive/Handwashing with soap.csv")
df_open_defecation = pd.read_csv("archive/Open defecation.csv")

dataframe_dict = {"Titles": ["Drinking_water_dataframe", "Sanitation_services_dataframe", "Handwashing_dataframe", "Open_defecation"],
              "Dataframes": ['drinking', 'sanitation', 'handwashing', 'open_defecation'] }

dataframe_table = pd.DataFrame(dataframe_dict)

# Function to get minimum and maximum year value in each dataframe
for dataframe in dataframe_table["Dataframes"]:
    if dataframe == "drinking":
        min_year = df_drinking["Year"].min()
        max_year = df_drinking["Year"].max()
    elif dataframe == "sanitation":
        min_year = df_sanitation["Year"].min()
        max_year = df_sanitation["Year"].max()
    elif dataframe == "handwashing":
        min_year = df_handwashing["Year"].min()
        max_year = df_handwashing["Year"].max()
    else:
        min_year = df_open_defecation["Year"].min()
        max_year = df_open_defecation["Year"].max()

# CSS styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    # The interactive plotly map
    html.Div(className="row", children=[

        html.Div(className="six columns", children=[
        # The Dropdown to select the dataframes
            dcc.Dropdown(#options=['df_drinking', 'df_handwashing'],
                options=dataframe_table["Dataframes"].unique(),
                value='drinking',
                id="dataframe_dropdown",
                style={"width": "50%", "display": "inline-block"})
        ]),

        html.Div(className="six columns", children=[
        # The Dropdown to select a value from the Residence Type column
            dcc.Dropdown(
                options=["Total", "Urban", "Rural"],
                value="Total",
                id="residence_area_type",
                style={"width": "40%", "display": "inline-block"}
            )
        ])
    ]),

    html.Br(),

    html.Div(id="dataframe_dropdown_output"),

    html.Br(),

    # The interactive plotly map
    dcc.Graph(id="sanitation_map"),

    # Add slider for year
    dcc.Slider(min=min_year, max=max_year, value=min_year, step=None, marks={str(year): str(year) for year in range(min_year, max_year + 1)},
               included=False, id="year_slider"),

    # The Line graph
    dcc.Graph(id="line_graph")

])

# Show the selected dataframe
@app.callback(
    Output("dataframe_dropdown_output", "children"),
    Input("dataframe_dropdown", "value"),
    Input("residence_area_type", "value")
)
def dropdown_output(value, residence_value):
    return f"You have chosen the {value} dataframe and the {residence_value} Residence Area Type option"

# Draw a plotly map based on the dropdown value chosen
@app.callback(
    Output("sanitation_map", "figure"),
    Input("dataframe_dropdown", "value"),
    Input("year_slider", "value"),
    Input("residence_area_type", "value")
)
def choropleth_map(dataframe_dropdown, year_slider, residence_area_type):
    if dataframe_dropdown == "drinking":
        df = df_drinking
    elif dataframe_dropdown == "sanitation":
        df = df_sanitation
    elif dataframe_dropdown == "handwashing":
        df = df_handwashing
    else:
        df = df_open_defecation

    dff = df[df["Year"] == year_slider]
    dff = dff[dff["Residence Area Type"] == residence_area_type]
    dff = dff.sort_values(by="Year")

    fig = px.choropleth(dff, locations="Country", locationmode="country names", color="Display Value", projection="mercator",
                       hover_name="Country", scope="world", width=1000, custom_data="Country")

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

# Draw the drinking line graph
## First create the function that will automatically plot the map based on country name (from hover), the dataframe
## selected (from dropdown) and the residence type (from dropdown also)
def check_dropdown(dataframe_dropdown):
    if dataframe_dropdown == "drinking":
        df = df_drinking
    elif dataframe_dropdown == "sanitation":
        df = df_sanitation
    elif dataframe_dropdown == "handwashing":
        df = df_handwashing
    else:
        df = df_open_defecation

    return df


# Now create the graph that updates the country name based on hover and showing Years on x-axis and Display value
# of chosen dataframe on y-axis
@app.callback(
    Output("line_graph", "figure"),
    Input("sanitation_map", "clickData"),
    Input("dataframe_dropdown", "value"),
    Input("residence_area_type", "value"),
)
def create_graph(clickData, dataframe_dropdown, residence_area_type):
    if clickData is None:
        country_name = "Kenya"
    else:
        country_name = clickData["points"][0]["hovertext"]

    # country_name = clickData["points"][0]["customdata"]
    df = check_dropdown(dataframe_dropdown)

    dff = df[df["Country"] == country_name]
    dff = dff[dff["Residence Area Type"] == residence_area_type]

    dff.sort_values(by="Year")
    #
    fig = px.line(dff, x="Year", y="Display Value", markers=True)

    fig.update_layout(title=dict(text=f"{dff['Indicator'].iloc[0]} for {country_name} and Residence Type {residence_area_type}"))

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)


































































