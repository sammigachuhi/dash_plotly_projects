from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('sanitation_long2.csv')

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div("App that shows Percentage Distribution of Human Waste Disposal Across Counties (2019 Census)"),

    html.Hr(),

    html.Div([
        dcc.Dropdown(
            df['County'].unique(),
            'BARINGO',
            id='dropdown',
        )
    ]),

    html.Hr(),

    dcc.Graph(id='graph-based-on-dropdown')
])

@app.callback(
    Output('graph-based-on-dropdown', 'figure'),
    Input('dropdown', 'value'),
)
def update_figure(selected_county):
    filtered_county = df[df.County == selected_county]
    # filtered_indicator = df[df.indicator == selected_indicator]

    fig = px.bar(filtered_county, x='indicator',
                 y='value', color='indicator',
                 title="Percentage Distribution of Conventional Households by Main Mode of Human Waste Disposal According to Kenya 2019 Census",
                 height=600)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)



























