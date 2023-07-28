# Import the required packages
import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# Source of the data used is:
# Clean the dataset for: "D:\gachuhi\dash-projects\dash-layout\data\diarrhoea_children_gdp.csv"
# Specifically the CSV file: "diarrhoea_children_gdp.csv"

# Remove all rows that have null values in the column: "Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)" and "Population (historical estimates)"

df = pd.read_csv("data/diarrhoea_children_gdp.csv")
# print(df)

# Now remove all null values in the column: "Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)" and "Population (historical estimates)"
# df = df.copy()
df = df.dropna(subset=["Deaths - Diarrheal diseases - Sex: Both - Age: Under 5 (Rate)", "Population (historical estimates)"])
print(df)

# Save the cleaned dataframe
# df.to_csv("data/cleaned_df.csv")

# Now to create the plotly dashboard
app = Dash(__name__)
server = app.server

# Create the layout
app.layout = html.Div([

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
    )

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
                        title=f"Map showing deaths from diarrhoeal diseases for children <5 years in {year_slider}")

    fig.update_layout(transition={"easing": "elastic-out"})

    return fig

if __name__ == "__main__":
    app.run(debug=True)


























































































