# Import the necessary python dash modules
from dash import Dash, dcc, dash_table, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('sanitation_long2.csv')
df2 = pd.read_csv('human_waste_filtered.csv')

app = Dash(__name__)

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

    dash_table.DataTable(data=df2.to_dict('records'), page_size=5),

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






























