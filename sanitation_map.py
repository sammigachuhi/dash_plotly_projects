import plotly.express as px
import pandas as pd
from dash import Dash, dcc, Input, Output, html

# The sanitation dataframes from Kaggle: https://www.kaggle.com/datasets/navinmundhra/world-sanitation
df_drinking = pd.read_csv("archive/Basic and safely managed drinking water services.csv")
df_sanitation = pd.read_csv("archive/Basic and safely managed sanitation services.csv")
df_handwashing = pd.read_csv("archive/Handwashing with soap.csv")
df_open_defecation = pd.read_csv("archive/Open defecation.csv")

# This dictionary will help in matching the string options from the dash dropdown to the correct datasets
dataframe_dict = {"Titles": ["Drinking_water_dataframe", "Sanitation_services_dataframe", "Handwashing_dataframe", "Open_defecation"],
              "Dataframes": ['drinking', 'sanitation', 'handwashing', 'open_defecation'] }

# Convert the `dataframe_dict` dictionary to a pandas dataframe
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
server = app.server

# Layout for our data visualization application
app.layout = html.Div(children=[
    # Title for the data visualization app showing a map of sanitation indicators worldwide by year and a graph for trend
    # of sanitation indicators by country
    html.H2("Data Visualization showing trend of sanitation indicators by country and year worldwide"),

    html.Br(),

    # Show source of the sanitation data
    dcc.Markdown(
        '''
        The dataset used in creating this visualization has been sourced 
        from [Kaggle](https://www.kaggle.com/datasets/navinmundhra/world-sanitation)
        ''',
        link_target="_blank"
    ),

    html.Br(),

    # The dataframe and residence type dropdowns
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
    dcc.Graph(id="sanitation_map", style={"padding": 20}),

    html.Br(),

    # Add slider for year
    dcc.Slider(min=min_year, max=max_year, value=min_year, step=None, marks={str(year): str(year) for year in range(min_year, max_year + 1)},
               included=False, id="year_slider"),

    # The Line graph
    dcc.Graph(id="line_graph"),

    html.Br(),

    # The button to download the dataframe selected in the dropdown
    html.Div([
        html.Button("Download CSV Dataframe in Dropdown", id="btn_csv"),
        dcc.Download(id="download_selected_dataframe")
    ])

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

    fig = px.choropleth(dff, locations="Country", locationmode="country names", color="Display Value", projection="orthographic",
                       hover_name="Country", scope="world", width=1000, custom_data="Country")

    fig.update_layout(margin={"r": 0, "l": 0, "b": 0}, title={"text": f"World Sanitation and Health by Country in {year_slider}"})

    return fig

# Draw the drinking line graph
## First create the function that will automatically plot the map based on country name (from hover), the dataframe
## selected (from dropdown) and the residence type (from dropdown also). Thanks to Stack Overflow at
# this link: https://stackoverflow.com/questions/76639315/make-the-line-graph-update-based-on-the-country-clicked-on-the-plotly-choropleth/76639830?noredirect=1#comment135126637_76639830

# The below custom function matches the string selected in the dash dropdown to the correct dataframe
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

    fig.update_layout(
        title=dict(text=f"{dff['Indicator'].iloc[0]} for {country_name} and Residence Type - {residence_area_type} for years: ({dff['Year'].min()}-{dff['Year'].max()})"))

    return fig

# The function to download the dataframe selected in the dropdown
@app.callback(
    Output("download_selected_dataframe", "data"),
    Input("btn_csv", "n_clicks"),
    Input("dataframe_dropdown", "value"),
    prevent_initial_call=True
)
def download_dataframe_dropdown(n_clicks, dataframe_dropdown):
    df = check_dropdown(dataframe_dropdown) # Reusing the `checkdown` function to match the dropdown selection to the
    # the correct dataframe

    # Send the dataframe selected in dropdown to computer directory as CSV file, with prefix of dataframe selected in
    # dropdown
    return dcc.send_data_frame(df.to_csv, f"{dataframe_dropdown}.csv")

if __name__ == "__main__":
    app.run_server(debug=True)


































































