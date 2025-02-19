from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash()

# Mock function to get different data for different timeframes
def get_data(timeframe):
    if timeframe == "1H":
        return pd.DataFrame({"Fruit": ["Apples", "Oranges", "Bananas"], "Amount": [4, 2, 3], "City": ["SF", "SF", "SF"]})
    elif timeframe == "4H":
        return pd.DataFrame({"Fruit": ["Apples", "Oranges", "Bananas"], "Amount": [5, 1, 4], "City": ["Montreal", "Montreal", "Montreal"]})
    else:
        return pd.DataFrame({"Fruit": ["Apples", "Oranges", "Bananas"], "Amount": [2, 4, 5], "City": ["SF", "Montreal", "SF"]})

app.layout = html.Div([
    html.Div([
        "Select Timeframe: ",
        dcc.Dropdown(['1H', '4H', '1D'], '1H', id='timeframe-dropdown')
    ]),
    html.Br(),
    dcc.Graph(id='example-graph')
])

@callback(
    Output('example-graph', 'figure'),
    Input('timeframe-dropdown', 'value')
)
def update_data(timeframe):
    df = get_data(timeframe)
    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    return fig

if __name__ == '__main__':
    app.run(debug=True)
