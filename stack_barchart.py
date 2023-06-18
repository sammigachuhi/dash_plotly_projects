# Import the necessary packages
import pandas as pd
import plotly.express as px
from dash import Dash, dash_table, dcc, html, Input, Output

df = pd.read_csv('sanitation_long2.csv')
df2 = pd.read_csv('human_waste_filtered.csv')
df2 = df2[['County', 'Conventional Households', 'Main Sewer', 'Septic tank', 'Cess pool', 'VIP Latrine',
           'Pit latrine covered', 'Pit Latrine uncovered', 'Bucket latrine', 'Open/ Bush', 'Bio-septic tank/ Biodigester', 'Not Stated']]

# Initialize the app
app = Dash(__name__)
server = app.server

# App layout
app.layout = html.Div([
    html.H2(children="Pie chart showing human waste disposal as proportion of conventional households (Kenya 2019 census)"),

    # Create dropdown
    dcc.Dropdown([name for name in df.County], id='selected_county', multi=True),

    # Create stack bar graph/chart
    dcc.Graph(figure={}, id='controls-and-graph'),

    # Create filterable datatable
    dash_table.DataTable(columns= [
        {'name': i, 'id': i} for i in df2.columns
    ],
        data=df2.to_dict('records'),
        filter_action='native',
        sort_action='native',
        page_size=5),

    # Create download button
    html.Div([
        html.Button("Download CSV", id='btn-csv'),
        dcc.Download(id='download-dataframe-csv')
    ])
])

@app.callback(
    Output('controls-and-graph', 'figure'),
    Input('selected_county', 'value'),
)
def update_graph(dropdown_choices):
    if isinstance(dropdown_choices, list):
        dff = df[df.County.isin(dropdown_choices)]
        fig = px.bar(dff, x='County', y='value', color='indicator')
        fig.update_layout(transition_duration=50)
        return fig
# def update_graph(dropdown_choices):
#     dff = df[df.County == dropdown_choices]
#     fig = px.bar(dff, x='County', y='value', color='indicator')
#     return fig

# Function to show and download dataframe
@app.callback(
    Output('download-dataframe-csv', 'data'),
    Input('btn-csv', 'n_clicks'),
    prevent_initial_call=True
)
def func(n_clicks):
    return dcc.send_data_frame(df2.to_csv, 'mydf.csv')

if __name__ == '__main__':
    app.run_server(debug=True)































