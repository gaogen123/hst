import backtrader as bt

class tdx_datasource(bt.feeds.PandasData):
    lines = (
        'turnover'
        ,
    )
    params = (
        ('datetime', 'datetime'),
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'vol'),
        ('openinterest', -1),
        ('turnover', 'hsl'),
    )