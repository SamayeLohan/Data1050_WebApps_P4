import dash
from dash import dash_table
from dash import dcc # dash core components
from dash import html
from dash.dependencies import Input, Output

import pandas as pd

df = pd.read_csv('https://bit.ly/elements-periodic-table')

app = dash.Dash(__name__)
def identity(x): return x

columns = df.columns

app.layout = html.Div(children=[
    html.H2(children='Pivot Table'),
    dcc.Dropdown(
        id="index_dropdown",
        options=[{'label': index, 'value': index} for index in columns],
        multi=False,
        placeholder='Select Index'
    ),
    dcc.Dropdown(
        id="column_dropdown",
        options=[{'label': column, 'value': column} for column in columns],
        multi=False,
        placeholder='Select Column'
    ),
    dcc.Dropdown(
        id="value_dropdown",
        options=[{'label': value, 'value': value} for value in columns],
        multi=False,
        placeholder='Select Value'
    ),
    html.Div(id='data'),
])

@app.callback(
    Output('data', 'children'),
    [Input('index_dropdown', 'value'), 
     Input('column_dropdown', 'value'), 
     Input('value_dropdown', 'value')]
)
def update_output(i, c, v):
        pt = df.pivot_table(index=i, columns=c, values=v, aggfunc=identity)
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in pt.columns],
                data=pt.reset_index().to_dict('rows')
            )
        ])
    

app.run_server(debug=True, host="0.0.0.0")
