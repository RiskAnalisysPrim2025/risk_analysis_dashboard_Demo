# Risk Analysis Dashboard

A comprehensive financial risk analysis dashboard built with Python and Dash that provides portfolio risk monitoring with multiple variance models and predictive confidence intervals.

## Features

- **Real-time Portfolio Tracking**: Monitor portfolio performance using Yahoo Finance data
- **Multiple Risk Models**: Choose from Historic, Moving Average (MA), Exponentially Weighted Moving Average (EWMA), ARCH, and GARCH models
- **Predictive Analytics**: Generate future portfolio value predictions with confidence intervals
- **Interactive Dashboard**: User-friendly web interface with dark/light theme support
- **Responsive Design**: Modern UI with Bootstrap components and Font Awesome icons

## Project Structure

```
risk_analysis_dashboard_Demo/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main Dash application
│   └── assets/
│       └── style.css        # Additional styles
├── src/
│   ├── __init__.py
│   ├── portfolio.py         # Portfolio management class
│   └── models/              # Risk models implementation
│       ├── __init__.py
│       ├── abstract_model.py
│       ├── arch_model.py    # ARCH model
│       ├── ewma_model.py    # EWMA model
│       ├── garch_model.py   # GARCH model
│       ├── ma_model.py      # Moving Average model
│       └── model.py         # Base historic model
├── notebooks/
│   └── 01_asset_selection.ipynb  # Jupyter notebook for analysis
├── config.py                # Portfolio and model configuration
└── requirements.txt         # Python dependencies
```

## Requirements

- Python 3.8 or higher
- Internet connection (for fetching financial data)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd risk_analysis_dashboard_Demo
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The portfolio configuration is managed in `config.py`:

```python
portfolio_config = {
    'AAPL': 4,  # 4 shares of Apple
    'MSFT': 5   # 5 shares of Microsoft
}

model_config = {
    "ma_params": {"window": 20},
    "ewma_params": {"lambda": 0.89},
    "arch_params": {"p": 1},
    "garch_params": {"p": 1, "q": 1},
}
```

You can modify these configurations to track different assets and adjust model parameters.

## Running the Application

1. **Start the dashboard**:
   ```bash
   python app.main
   ```

2. **Access the application**:
   - Open your web browser
   - Navigate to `http://127.0.0.1:8050`

3. **Using the dashboard**:
   - **Timeframe**: Select data granularity (1h for hourly, 1d for daily)
   - **Period**: Choose the historical data period (1d, 5d, 1mo, 3mo, 1y)
   - **Variance Model**: Select the risk model for predictions
   - **Future Periods**: Set the number of periods to predict
   - Click **Apply** to update the visualization
   - Use the **Reset** button to return to default settings
   - Toggle between light/dark themes using the moon/sun icon

## Risk Models

The dashboard supports five different variance models:

- **Historic**: Uses historical variance for predictions
- **MA (Moving Average)**: Simple moving average of returns
- **EWMA (Exponentially Weighted Moving Average)**: Gives more weight to recent observations
- **ARCH**: Autoregressive Conditional Heteroskedasticity model
- **GARCH**: Generalized ARCH model with both autoregressive and moving average components

## Dependencies

- `plotly~=6.0.0` - Interactive plotting library
- `pandas~=2.2.3` - Data manipulation and analysis
- `dash~=2.18.2` - Web application framework
- `yfinance~=0.2.65` - Yahoo Finance data downloader
- `numpy~=2.3.3` - Numerical computing
- `dash-bootstrap-components~=2.0.4` - Bootstrap components for Dash
- `scipy~=1.16.1` - Scientific computing library

## Troubleshooting

1. **Data not loading**: Ensure you have an active internet connection for Yahoo Finance API
2. **Module not found errors**: Verify all dependencies are installed with `pip install -r requirements.txt`
3. **Port conflicts**: If port 8050 is in use, the application will automatically try other ports

## License

This project is for educational and demonstration purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

© 2025 Risk Monitor Dashboard
