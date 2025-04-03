
portfolio_config  = {
    'AAPL':4,
    'MSFT':5
}

model_config = {
    "ma_params":{"window":20},
    "ewma_params": {"lambda": 0.89},
    "arch_params": {"p": 1},
    "garch_params": {"p": 1,"q":1},
}