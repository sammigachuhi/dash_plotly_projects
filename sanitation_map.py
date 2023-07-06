import plotly.express as px
import pandas as pd
from dash import Dash, dcc, Input, Output, html

df_drinking = pd.read_csv("archive/Basic and safely managed drinking water services.csv")
df_sanitation = pd.read_csv("archive/Basic and safely managed sanitation services.csv")
df_handwashing = pd.read_csv("archive/Handwashing with soap.csv")
df_open_defecation = pd.read_csv("archive/Open defecation.csv")

dataframes = {"Drinking_water_dataframe": df_drinking,
              "Sanitation_services_dataframe": df_sanitation,
              "Handwashing_dataframe": df_handwashing,
              "Open_defecation": df_open_defecation}

dataframe_dict = {"Titles": ["Drinking_water_dataframe", "Sanitation_services_dataframe", "Handwashing_dataframe", "Open_defecation"],
              "Dataframes": ['df_drinking', 'df_sanitation', 'df_handwashing', 'df_open_defecation'] }
dataframe_table = pd.DataFrame(dataframe_dict)

# Function to get minimum and maximum year value in each dataframe
for dataframe in dataframe_table["Dataframes"]:
    if dataframe == "df_drinking":
        min_year = df_drinking["Year"].min()
        max_year = df_drinking["Year"].max()
    elif dataframe == "df_sanitation":
        min_year = df_sanitation["Year"].min()
        max_year = df_sanitation["Year"].max()
    elif dataframe == "df_handwashing":
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
                value='df_drinking',
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
    dcc.Slider(min=min_year, max=max_year, value=min_year, step=1, marks={str(year): str(year) for year in range(min_year, max_year + 1)},
               included=False, id="year_slider")
])

# Show the selected dataframe
@app.callback(
    Output("dataframe_dropdown_output", "children"),
    Input("dataframe_dropdown", "value")
)
def dropdown_output(value):
    return f"You have chosen the {value} dataframe"

# Draw a plotly map based on the dropdown value chosen
@app.callback(
    Output("sanitation_map", "figure"),
    Input("dataframe_dropdown", "value"),
    Input("year_slider", "value"),
    Input("residence_area_type", "value")
)
def choropleth_map(dataframe_dropdown, year_slider, residence_area_type):
    if dataframe_dropdown == "df_drinking":
        df = df_drinking
    elif dataframe_dropdown == "df_sanitation":
        df = df_sanitation
    elif dataframe_dropdown == "df_handwashing":
        df = df_handwashing
    else:
        df = df_open_defecation

    dff = df[df["Year"] == year_slider]
    dff = dff[dff["Residence Area Type"] == residence_area_type]
    dff = dff.sort_values(by="Year")

    fig = px.choropleth(dff, locations="Country", locationmode="country names", color="Display Value", projection="mercator",
                        scope="world", width=1000)

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)




































































