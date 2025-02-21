from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
from config import portfolio_config
from src.portfolio import Portfolio
from src.models.model import Model
app = Dash()

portfolio = Portfolio(portfolio_config)

naive_model = Model(portfolio)

app.layout = html.Div([
    html.H1("Dashboard Análisis de Riesgo"),

    html.Div([
        "Select Timeframe: ",
        dcc.Dropdown(['1h', '1d'], '1h', id='timeframe-dropdown')
    ]),

    html.Div([
        "Select Period: ",
        dcc.Dropdown(['1d', '5d', '1mo', '3mo'], '1d', id='period-dropdown')
    ]),

    html.Div([
        "Select Model: ",
        dcc.Dropdown(['naive'], 'naive', id='model-dropdown')
    ]),

    html.Div([
        "Future Periods: ",
        dcc.Input(id='future-periods-input', type='number', value=5, min=0, step=1)
    ]),

    html.Br(),
    dcc.Graph(id='graph')
])


@callback(
    Output('graph', 'figure'),
    [Input('timeframe-dropdown', 'value'),
     Input('period-dropdown', 'value'),
     Input('model-dropdown', 'value'),
     Input('future-periods-input', 'value')]
)
def update_data(timeframe, period, model, future_periods):
    df = portfolio.get_data(timeframe, period)
    print(model, future_periods)

    match model:
        case 'naive':
            current_model = naive_model
        case _ :
            current_model = naive_model


    print(current_model.get_variance(timeframe, period))

    # Verificamos si df no es None
    if df is None or df.empty:
        return px.line(title="No hay datos disponibles")

    # Eliminar NaN y resetear el índice para compactar los datos
    df = df.reset_index()
    df.columns = ["Index", "Value"]  # Renombramos para evitar problemas

    # Graficamos sin huecos en el tiempo
    fig = px.line(df, x=df.index, y="Value", title="Evolución del Portafolio")
    fig.update_xaxes(title_text="Tiempo")
    fig.update_yaxes(title_text="Valor del Portafolio")

    return fig


if __name__ == '__main__':
    app.run(debug=True)
