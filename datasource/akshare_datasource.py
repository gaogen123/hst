import backtrader as bt

class akshare_datasource(bt.feeds.PandasData):
    lines = (
        'turnover',
        'code',
    )
    params = (
        ('datetime', 'datetime'),
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'vol'),
        ('turnover', 'hsl'),
        ('code', 'code_1'),
    )
