import backtrader as bt

class tdx_datasource(bt.feeds.PandasData):
    lines = (
        'turnover',
        'code'
        ,
    )
    params = (
        ('datetime', 'datetime'),
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'vol'),
        ('code', 'code'),
        ('turnover', 'hsl'),
    )