import backtrader as bt

class hst_datasource(bt.feeds.PandasData):
    lines = ('turnover',)
    params = (
        ('datetime', 'date'),
        ('open', 'openPrice'),
        ('high', 'highPrice'),
        ('low', 'lowPrice'),
        ('close', 'closePrice'),
        ('volume', 'volume'),
        ('openinterest', -1),
        ('turnover', 'turnover'),
    )

