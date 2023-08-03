# Import the required packages
import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import json
import time

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# Source of the data used is: https://ourworldindata.org/childhood-diarrheal-diseases?utm_source=pocket_saves
# from the download section of compound line graph

# Clean the dataset for: "D:\gachuhi\dash-projects\dash-layout\data\diarrhoea_children_gdp.csv"
# Specifically the CSV file: "diarrhoea_children_gdp.csv"

# Remove all rows that have null values in the column: "Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)"
# and "Population (historical estimates)"

df = pd.read_csv("data/diarrhoea_children_gdp.csv")
# print(df)

# Now remove all null values in the column: "Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)" and
# "Population (historical estimates)"
# df = df.copy()
df = df.dropna(
    subset=["Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)", "Population (historical estimates)"])
# print(df)

# The below dataset contains country codes and their continents. We want to join the countries in our diarrhoea dataset
# to their sub-regions since the `continent` column in our diarrhoea dataset has missing values
df_code = pd.read_csv("https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv")
df_code["Code"] = df_code["alpha-3"]

df = pd.merge(df, df_code[["Code", "sub-region"]], on="Code", how="left") # Merge with country `Code` to their continents

# Remove all rows with value `None` in column `sub-region`
df = df.dropna(subset=["sub-region"])

# Save the cleaned dataframe
# df.to_csv("data/cleaned_df2.csv")

# Now to create the plotly dashboard
app = Dash(__name__)
server = app.server

# Create the layout
app.layout = html.Div([

    #0 The heading
    html.H2(f"Diarrhoea related deaths amongst children <5 years, World"),

    html.Br(),

    dcc.Markdown("""
    Source: [Our World in Data](https://ourworldindata.org/childhood-diarrheal-diseases?utm_source=pocket_reader)
    
    Our World In Data is a project of the Global Change Data Lab, a registered charity in England 
    and Wales (Charity Number 1186433).
    """,
                 link_target="_blank"),

    #1 the map layout
    dcc.Graph(id="map-year"),

    #2 The slider
    dcc.Slider(
        df["Year"].min(),
        df["Year"].max(),
        step=None,
        id="year-slider",
        value=df["Year"].max(),
        marks={str(year): str(year) for year in df["Year"].unique()}
    ),

    #3 The heatmap and scatterplot on the same column
    html.Div([
        dcc.Graph(id="heat-map-country-year"),
        dcc.Graph(id="scatterplot-death-gdp-year")
    ]),

    html.Br(),

    ###### This is to help in debugging capturing the clicked country on the choropleth map
    # html.Div([
    #     dcc.Markdown("""
    #             **Click Data**
    #
    #             Click on points in the graph.
    #             """),
    #     html.Pre(id='click-data', style=styles['pre']),
    #     ], className='three columns'),
    ##########

    #4 Draw line graph of population of selected country dependent on country selected on map and likewise for
    # gdp per capita in one row
    html.Div([
        dcc.Graph(id="line-graph-population", style={"width": "48%", "display": "inline-block"}),
        dcc.Graph(id="line-graph-gdp-capita", style={"width": "48%", "display": "inline-block"})
    ]),

    #5 Draw bar graph of diarrhoea related deaths across the years
    dcc.Graph(id="diarrhoea-bar-graph"),

])

# Callbacks section
## Callback for #1 The map layout
@app.callback(
    Output("map-year", "figure"),
    Input("year-slider", "value")
)
def update_map(year_slider):
    dff = df[df["Year"] == year_slider]

    fig = px.choropleth(dff, locations="Entity", locationmode="country names",
                        color="Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)",
                        hover_name="Year",
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title=f"Map showing deaths from diarrhoeal diseases for children <5 years in {year_slider}",
                        custom_data=["Entity"],
                        labels={
                            "Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)": "Deaths"})

    fig.update_layout(transition={"easing": "elastic-out"})

    return fig

# Callbacks for #3 heatmap and scatterplot on the same page
# Heatmap callback
@app.callback(
    Output("heat-map-country-year", "figure"),
    Input("year-slider", "value")
)
def update_heatmap(year_slider):
    dff = df[df["Year"] == year_slider]

    fig = px.treemap(dff, names="Entity", path=["sub-region", "Entity"],
                     values="Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)",
                     color="Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)", hover_name="Year",
                     hover_data="GDP per capita, PPP (constant 2017 international $)",
                     color_continuous_scale=px.colors.sequential.Plasma,
                     color_continuous_midpoint=np.average(
                         dff["Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)"],
                         weights=dff["GDP per capita, PPP (constant 2017 international $)"]),
                     title=f"Treemap Chart showing deaths from diarrhoeal diseases" + "<br>" +
                           f"for children <5 years in {year_slider}",
                     labels={"Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)": "Deaths"})

    fig.update_layout(transition={"easing": "elastic-out",
                                  "duration": 50},
                      margin={"t":50, "l":25, "r":25, "b":25})

    return fig

# Scatterplot callback
@app.callback(
    Output("scatterplot-death-gdp-year", "figure"),
    Input("year-slider", "value")
)
def update_scatterplot(year_slider):

    dff = df[df["Year"] == year_slider]

    fig = px.scatter(dff, x="GDP per capita, PPP (constant 2017 international $)",
                     y="Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)",
                     color="sub-region",
                     size="Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)", hover_name="Entity",
                     hover_data="GDP per capita, PPP (constant 2017 international $)",
                     title=f"Scatterplot showing Deaths from Diarrhoea cases against GDP per capita," + "<br>" +
                           f"PPP (constant 2017 international $ for {year_slider}",
                     labels={"Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)": "Deaths"})

    fig.update_layout(transition={"easing": "elastic-out",
                                  "duration": 50})

    return fig

########
# @app.callback(
#     Output('click-data', 'children'),
#     Input('map-year', 'clickData'))
# def display_click_data(clickData):
#     return json.dumps(clickData, indent=2)

######

#4.1 Callback for line graph for population against years
@app.callback(
    Output("line-graph-population", "figure"),
    Input("map-year", "clickData")
)
def line_population(clickData):
    if clickData is None:
        country_name = "Kenya"
    else:
        country_name = clickData["points"][0]["location"]

    dff = df[df["Entity"] == country_name]
    dff = dff.sort_values(by="Year")
    #
    fig = px.line(dff, x="Year", y="Population (historical estimates)", markers=True,
                  )
    #
    fig.update_layout(
        title={"text": f"Population (historical estimates) for {country_name}" + "<br>" +
                       f"({dff['Year'].min()} - {dff['Year'].max()})"}
    )
    #
    return fig

#4.2 Callback for line graph for gdp-per-capita against years
@app.callback(
    Output("line-graph-gdp-capita", "figure"),
    Input("map-year", "clickData")
)
def line_capita(clickData):
    if clickData is None:
        country_name = "Kenya"
    else:
        country_name = clickData["points"][0]["location"]

    dff = df[df["Entity"] == country_name]
    dff = dff.sort_values(by="Year")

    fig = px.line(dff, x="Year", y="GDP per capita, PPP (constant 2017 international $)", markers=True,
                  labels={"GDP per capita, PPP (constant 2017 international $)": "GDP per Capita"})

    fig.update_layout(
        title={
            "text": f"GDP per capita, PPP (constant 2017 international $)" + "<br>" +
                    f"for {country_name} ({dff['Year'].min()} - {dff['Year'].max()})"}
    )

    return fig

#5 Callbacks to draw bar graph for diarrhoea related deaths
@app.callback(
    Output("diarrhoea-bar-graph", "figure"),
    Input("map-year", "clickData")
)
def update_bar_graph(clickData):
    if clickData is None:
        country_name = "Kenya"
    else:
        country_name = clickData["points"][0]["location"]

    dff = df[df["Entity"] == country_name]
    dff = dff.sort_values(by="Year")

    fig = px.bar(dff, x="Year", y="Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)",
                 hover_data=["GDP per capita, PPP (constant 2017 international $)", "Population (historical estimates)",
                             "sub-region"],
                 labels={"Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)": "Deaths"},
                 color="Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)")

    fig.update_layout(title={"text": f"Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)" + "<br>" +
                                     f"for {country_name} ({dff['Year'].min()} - {dff['Year'].max()})"})


    return fig

if __name__ == "__main__":
    app.run(debug=True)


























































































