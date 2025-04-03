import numpy as np
from dash import Dash, dcc, html, Input, Output, callback, State
import plotly.express as px
from config import portfolio_config, model_config
from src.portfolio import Portfolio
from src.models.model import Model
from src.models.ma_model import MAModel
from src.models.ewma_model import EWMAModel
from src.models.arch_model import ARCHModel
from src.models.garch_model import GARCHModel
import dash_bootstrap_components as dbc
import scipy.stats as stats

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

portfolio = Portfolio(portfolio_config)
hist_model = Model(portfolio)
ma_model = MAModel(portfolio,**model_config.get('ma_params'))
ewma_model = EWMAModel(portfolio,**model_config.get('ewma_params'))
arch_model = ARCHModel(portfolio,**model_config.get('arch_params'))
garch_model = GARCHModel(portfolio,**model_config.get('garch_params'))


app.layout = html.Div([
    dcc.Store(id='theme-store', data={'mode': 'light'}),

    html.Link(
        rel='stylesheet',
        href='https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
    ),
    html.Link(
        rel='stylesheet',
        href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
    ),

    html.Div([
        html.Div([
            html.H1("RISK MONITOR", className="dashboard-title"),
            html.Button(
                html.I(className="fas fa-moon"),
                id='theme-switch',
                className='theme-btn'
            ),
        ], className="header-container"),

        html.Div([
            html.Div([
                html.H3("Parameters", className="panel-title"),

                html.Div([
                    html.Label("Timeframe", className="input-label"),
                    dcc.Dropdown(['1h', '1d'], '1d', id='timeframe-dropdown', className="dashboard-dropdown"),
                ], className="input-container"),

                html.Div([
                    html.Label("Period", className="input-label"),
                    dcc.Dropdown(['1d', '5d', '1mo', '3mo','1y'], '1y', id='period-dropdown',
                                 className="dashboard-dropdown"),
                ], className="input-container"),

                html.Div([
                    html.Label("Variance Model", className="input-label"),
                    dcc.Dropdown(['Historic','MA','EWMA','ARCH','GARH'], 'Historic', id='model-dropdown', className="dashboard-dropdown"),
                ], className="input-container"),

                html.Div([
                    html.Label("Future Periods", className="input-label"),
                    dcc.Input(id='future-periods-input', type='number', value=40, min=0, step=1,
                              className="dashboard-input"),
                ], className="input-container"),

                html.Div(className="spacer"),

                html.Div([
                    html.Button("Apply", id="apply-btn", className="action-btn"),
                    html.Button("Reset", id="reset-btn", className="action-btn secondary"),
                ], className="action-container"),

            ], className="control-panel"),

            html.Div([
                html.H3("Portfolio Performance", className="panel-title"),
                dcc.Graph(id='graph', className="dashboard-graph")
            ], className="visualization-panel"),
        ], className="dashboard-container"),

        html.Div([
            html.P("© 2025 Risk Monitor Dashboard", className="footer-text"),
        ], className="footer-container"),
    ], id="theme-wrapper"),

], id="main-container")


@app.callback(
    Output('theme-store', 'data'),
    Input('theme-switch', 'n_clicks'),
    State('theme-store', 'data')
)
def toggle_theme(n_clicks, data):
    if n_clicks:
        return {'mode': 'dark' if data['mode'] == 'light' else 'light'}
    return data


@app.callback(
    [Output('theme-wrapper', 'className'),
     Output('theme-switch', 'children')],
    Input('theme-store', 'data')
)
def update_theme(data):
    if data['mode'] == 'dark':
        return 'theme-background dark-theme', html.I(className="fas fa-sun")
    else:
        return 'theme-background light-theme', html.I(className="fas fa-moon")


@callback(
    Output('graph', 'figure'),
    [Input('apply-btn', 'n_clicks'),
     Input('theme-store', 'data')],
    [State('timeframe-dropdown', 'value'),
     State('period-dropdown', 'value'),
     State('model-dropdown', 'value'),
     State('future-periods-input', 'value')]
)
def update_data(n_clicks, theme_data, timeframe, period, model, future_periods):
    df = portfolio.get_data(timeframe, period)

    match model:
        case 'Historic':
            current_model = hist_model
        case 'MA':
            current_model = ma_model
        case 'EWMA':
            current_model = ewma_model
        case 'ARCH':
            current_model = arch_model
        case 'GARH':
            current_model = garch_model
        case _:
            current_model = hist_model

    if df is None or df.empty:
        return px.line(title="No data available")

    plot_df = df.reset_index()
    plot_df.columns = ["Date", "Value"]

    dark_mode = theme_data['mode'] == 'dark'
    bg_color = '#282838' if dark_mode else '#ffffff'
    text_color = '#E0E0E0' if dark_mode else '#333333'
    grid_color = '#2D2D3F' if dark_mode else '#f0f0f0'

    fig = px.line(plot_df, x="Date", y="Value", title="Portfolio Evolution")

    fig.update_traces(
        hovertemplate='<b>Date:</b> %{x|%Y-%m-%d %H:%M:%S}<br><b>Value:</b> %{y:.2f}<extra></extra>',
        line=dict(width=3, color='#6236FF')
    )

    if future_periods > 0:
        import plotly.graph_objects as go
        from datetime import timedelta

        sigmas = current_model.get_variances(timeframe, period, future_periods)

        mu = np.log(df / df.shift(1)).mean()

        s_0 = df.iloc[-1]

        last_date = plot_df["Date"].iloc[-1]

        if timeframe == '1h':
            time_delta = timedelta(hours=1)
        else:
            time_delta = timedelta(days=1)

        future_dates = [last_date] + [last_date + (i + 1) * time_delta for i in range(future_periods)]

        expected_values = [s_0] + [s_0 * (1 + mu * dt) for dt in range(1, future_periods + 1)]

        confidence_levels = [0.99, 0.95, 0.90, 0.80, 0.50]

        base_color = 'rgba(98, 54, 255, {})'
        opacities = [0.1, 0.15, 0.2, 0.25, 0.3]

        fig.add_trace(
            go.Scatter(
                x=future_dates,
                y=expected_values,
                mode='lines',
                line=dict(color='#6236FF', width=2, dash='dash'),
                name='Expected Value',
                hovertemplate='<b>Date:</b> %{x|%Y-%m-%d %H:%M:%S}<br><b>Value:</b> %{y:.2f}<extra></extra>'
            )
        )

        for i, confidence in enumerate(confidence_levels):
            z_score = stats.norm.ppf(1 - (1 - confidence) / 2)

            upper_bounds = []
            lower_bounds = []

            upper_bounds.append(s_0)
            lower_bounds.append(s_0)

            for dt, (sigma, expected_value) in enumerate(zip(sigmas, expected_values[1:]), 1):
                std_dev = s_0 * sigma ** (1 / 2) * dt ** (1 / 2)

                upper = expected_value + z_score * std_dev
                lower = expected_value - z_score * std_dev

                upper_bounds.append(upper)
                lower_bounds.append(lower)

            x_values = future_dates + future_dates[::-1]

            y_values = upper_bounds + lower_bounds[::-1]

            fig.add_trace(
                go.Scatter(
                    x=x_values,
                    y=y_values,
                    fill='toself',
                    fillcolor=base_color.format(opacities[i]),
                    line=dict(color='rgba(0,0,0,0)'),
                    name=f'{int(confidence * 100)}% Confidence',
                    hoverinfo='skip'
                )
            )

    fig.update_layout(
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font_color=text_color,
        margin=dict(l=10, r=10, t=50, b=10),
        hovermode="closest",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor=bg_color,
            bordercolor=grid_color,
            borderwidth=1
        ),
        title={
            'font': {'size': 20, 'family': 'Inter, sans-serif', 'weight': 'bold'},
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'text': "Portfolio Evolution with Confidence Intervals",
            'font_color': text_color
        },
        xaxis={
            'showgrid': True,
            'gridcolor': grid_color,
            'zeroline': False,
            'color': text_color
        },
        yaxis={
            'title': "Portfolio Value",
            'showgrid': True,
            'gridcolor': grid_color,
            'zeroline': False,
            'title_font': {'size': 16, 'family': 'Inter, sans-serif'},
            'color': text_color,
            'title_font_color': text_color
        }
    )

    return fig

@app.callback(
    [Output('timeframe-dropdown', 'value'),
     Output('period-dropdown', 'value'),
     Output('model-dropdown', 'value'),
     Output('future-periods-input', 'value')],
    Input('reset-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_inputs(n_clicks):
    return '1h', '1d', 'naive', 5


app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Risk Monitor Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            :root {
                --primary-color: #6236FF;
                --secondary-color: #FF3A75;
                --success-color: #00C897;
                --bg-color: #F7F8FC;
                --panel-bg: #FFFFFF;
                --text-color: #333333;
                --border-color: #E0E0E0;
                --input-bg: #FFFFFF;
                --hover-color: #F0F0F0;
                --shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            }

            .dark-theme {
                --primary-color: #7C4DFF;
                --secondary-color: #FF4081;
                --success-color: #00E5B2;
                --bg-color: #1E1E2E;
                --panel-bg: #282838;
                --text-color: #E0E0E0;
                --border-color: #3F3F50;
                --input-bg: #363646;
                --hover-color: #32323F;
                --shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            }

            .dark-theme .dash-graph {
                background-color: var(--panel-bg);
            }

            .dark-theme .dash-spreadsheet {
                background-color: var(--panel-bg);
                color: var(--text-color);
            }

            .dark-theme .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner th,
            .dark-theme .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner td {
                background-color: var(--panel-bg);
                color: var(--text-color);
                border-color: var(--border-color);
            }

            body {
                font-family: 'Inter', sans-serif;
                margin: 0;
                padding: 0;
                transition: all 0.3s ease;
                background-color: #F7F8FC;
                color: #333333;
            }

            .theme-background {
                min-height: 100vh;
                width: 100%;
                background-color: var(--bg-color);
                color: var(--text-color);
                transition: all 0.3s ease;
            }

            .dash-dropdown .Select-control,
            .dash-dropdown .Select-menu-outer,
            .dash-dropdown .Select-value,
            .dash-dropdown .Select-placeholder,
            .dash-dropdown .Select-input > input {
                background-color: var(--input-bg) !important;
                color: var(--text-color) !important;
            }

            .dash-dropdown .Select-menu-outer .Select-option {
                background-color: var(--input-bg) !important;
                color: var(--text-color) !important;
            }

            .dash-dropdown .Select-menu-outer .Select-option.is-focused {
                background-color: var(--hover-color) !important;
            }

            #main-container {
                display: flex;
                flex-direction: column;
                min-height: 100vh;
                width: 100%;
            }

            #theme-wrapper {
                display: flex;
                flex-direction: column;
                min-height: 100vh;
                width: 100%;
            }

            .header-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px 40px;
                background-color: var(--panel-bg);
                box-shadow: var(--shadow);
                margin-bottom: 30px;
            }

            .dashboard-title {
                font-size: 28px;
                font-weight: 700;
                margin: 0;
                color: var(--primary-color);
                letter-spacing: 1.5px;
            }

            .theme-btn {
                background: transparent;
                border: none;
                cursor: pointer;
                font-size: 22px;
                color: var(--text-color);
                transition: transform 0.3s ease;
            }

            .theme-btn:hover {
                transform: rotate(30deg);
            }

            .dashboard-container {
                display: flex;
                gap: 30px;
                padding: 0 40px;
                flex: 1;
                margin-bottom: 30px;
            }

            .control-panel, .visualization-panel {
                background-color: var(--panel-bg);
                border-radius: 16px;
                box-shadow: var(--shadow);
                padding: 30px;
                display: flex;
                flex-direction: column;
            }

            .control-panel {
                width: 25%;
                min-width: 300px;
            }

            .visualization-panel {
                width: 75%;
                flex: 1;
            }

            .panel-title {
                font-size: 18px;
                font-weight: 600;
                margin-top: 0;
                margin-bottom: 25px;
                color: var(--text-color);
            }

            .input-container {
                margin-bottom: 24px;
            }

            .input-label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
                font-size: 14px;
                color: var(--text-color);
            }

            .dashboard-dropdown .Select-control,
            .dashboard-input {
                background-color: var(--input-bg);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
                color: var(--text-color);
                width: 100%;
                box-sizing: border-box;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
            }

            .dashboard-dropdown .Select-arrow-zone {
                padding-right: 0;
                position: absolute;
                right: 10px;
            }

            .dashboard-dropdown .Select-value {
                display: flex;
                align-items: center;
                line-height: normal;
                padding-top: 0;
                padding-bottom: 0;
                padding-right: 30px;
            }

            .dashboard-dropdown .Select-value-label {
                color: var(--text-color) !important;
                max-width: calc(100% - 30px);
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }

            .dashboard-dropdown .Select-clear-zone {
                position: absolute;
                right: 30px;
            }

            .dashboard-dropdown .Select {
                position: relative;
                width: 100%;
            }

            .dashboard-dropdown .Select-control {
                position: relative;
                overflow: hidden;
                min-height: 40px;
            }

            .dashboard-dropdown .Select-arrow {
                border-color: var(--text-color) transparent transparent;
                border-style: solid;
                border-width: 5px 5px 2.5px;
            }

            .dashboard-input:focus,
            .dashboard-dropdown .Select-control:hover {
                border-color: var(--primary-color);
                outline: none;
                box-shadow: 0 0 0 2px rgba(98, 54, 255, 0.15);
            }

            .dashboard-dropdown .Select-menu-outer {
                background-color: var(--input-bg);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                box-shadow: var(--shadow);
                margin-top: 5px;
                z-index: 10;
            }

            .dashboard-dropdown .Select-option {
                padding: 10px 12px;
                color: var(--text-color);
            }

            .dashboard-dropdown .Select-option.is-focused {
                background-color: var(--hover-color);
            }

            .dashboard-dropdown .Select-option.is-selected {
                background-color: var(--primary-color);
                color: white;
            }

            .dashboard-graph {
                height: 100%;
                width: 100%;
                min-height: 400px;
            }

            .spacer {
                flex: 1;
            }

            .action-container {
                display: flex;
                gap: 15px;
                margin-top: 15px;
            }

            .action-btn {
                background-color: var(--primary-color);
                color: white;
                border: none;
                padding: 12px 22px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                cursor: pointer;
                transition: all 0.2s ease;
                flex: 1;
            }

            .action-btn:hover {
                background-color: rgba(98, 54, 255, 0.85);
                transform: translateY(-2px);
            }

            .action-btn.secondary {
                background-color: transparent;
                color: var(--text-color);
                border: 1px solid var(--border-color);
            }

            .action-btn.secondary:hover {
                background-color: var(--hover-color);
            }

            .footer-container {
                padding: 20px 40px;
                text-align: center;
                font-size: 13px;
                color: var(--text-color);
                opacity: 0.7;
            }

            .visualization-panel .dash-graph {
                flex: 1;
                height: 100% !important;
            }

            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }

            ::-webkit-scrollbar-track {
                background: var(--bg-color);
            }

            ::-webkit-scrollbar-thumb {
                background: var(--border-color);
                border-radius: 4px;
            }

            ::-webkit-scrollbar-thumb:hover {
                background: var(--primary-color);
            }
        </style>
    </head>
    <body id="dash-body">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <script>
        </script>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)