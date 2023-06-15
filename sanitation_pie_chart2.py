# Import the necessary python dash modules
from dash import Dash, dcc, dash_table, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('sanitation_long2.csv')
df2 = pd.read_csv('human_waste_filtered.csv')
df2 = df2[['County', 'Conventional Households', 'Main Sewer', 'Septic tank', 'Cess pool', 'VIP Latrine',
           'Pit latrine covered', 'Pit Latrine uncovered', 'Bucket latrine', 'Open/ Bush', 'Bio-septic tank/ Biodigester', 'Not Stated']]

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H6("Pie chart showing human waste disposal as proportion of conventional households (Kenya 2019 census)"),

    html.Hr(),

    html.Div([
        dcc.Dropdown(
            df['County'].unique(),
            'BARINGO',
            id='select-county'
        )
    ]),

    dcc.Graph(id='indicator-graphic'),

    dash_table.DataTable(columns= [
        {'name': i, 'id': i} for i in df2.columns
        # {'name': 'County', 'id': 'County', 'type': 'text'},
        # {'name': 'Conventional Households', 'id': 'Conventional Households', 'type': 'text'},
        # {'name': 'Main Sewer', 'id': 'Main Sewer', 'type': 'numeric'},
        # {'name': 'Septic tank', 'id': 'Septic tank', 'type': 'numeric'},
        # {'name': 'Cess pool', 'id': 'Cess pool', 'type': 'numeric'},
        # {'name': 'VIP Latrine', 'id': 'VIP Latrine', 'type': 'numeric'},
        # {'name': 'Pit latrine covered', 'id': 'Pit latrine covered', 'type': 'numeric'},
        # {'name': 'Pit Latrine uncovered', 'id': 'Pit Latrine uncovered', 'type': 'numeric'},
        # {'name': 'Bucket latrine', 'id': 'Bucket latrine', 'type': 'numeric'},
        # {'name': 'Open/ Bush', 'id': 'Open/ Bush', 'type': 'numeric'},
        # {'name': 'Bio-septic tank/ Biodigester', 'id': 'Bio-septic tank/ Biodigester', 'type': 'numeric'},
        # {'name': 'Not Stated', 'id': 'Not Stated', 'type': 'numeric'}
],
        data=df2.to_dict('records'),
        filter_action='native',
        sort_action='native',
        page_size=5),


    html.Div([
        html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id='download-dataframe-csv'),
    ])

])

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('select-county', 'value'),
)
def update_graph(selected_county):
    filtered_df = df[df.County == selected_county]
    fig = px.pie(filtered_df, names='indicator', values='value')
    fig.update_layout(transition_duration=40)
    return fig

@app.callback(
    Output('download-dataframe-csv', 'data'),
    Input('btn_csv', 'n_clicks'),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df2.to_csv, 'mydf.csv')

if __name__ == '__main__':
    app.run_server(debug=True)