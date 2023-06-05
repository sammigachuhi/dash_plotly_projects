from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('sanitation_long2.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.Div("App that shows Percentage Distribution of Human Waste Disposal Across Counties"),

    html.Hr(),

    html.Div([
        dcc.Dropdown(
            df['County'].unique(),
            'BARINGO',
            id='dropdown',
        )
    ]),

    html.Hr(),

    # html.Div([
    #     dcc.RadioItems(
    #         options=['Conventional Households', 'Main Sewer', 'Septic tank',
    #                  'Cess pool', 'VIP Latrine', 'Pit latrine covered', 'Pit Latrine uncovered',
    #                  'Bucket latrine', 'Open/ Bush', 'Bio-septic tank/ Biodigester', 'Not Stated'],
    #         value='Main Sewer', id='radioitem'
    #     )
    # ]),

    dcc.Graph(id='graph-based-on-dropdown')
])

@app.callback(
    Output('graph-based-on-dropdown', 'figure'),
    Input('dropdown', 'value'),
    # Input('radioitem', 'value')
)
def update_figure(selected_county):
    filtered_county = df[df.County == selected_county]
    # filtered_indicator = df[df.indicator == selected_indicator]

    fig = px.bar(filtered_county, x='indicator',
                 y='value', color='indicator',
                 title="Percentage Distribution of Conventional Households by Main Mode of Human Waste Disposal")

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)



























