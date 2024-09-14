import backtrader as bt
import pyfolio as pf
import pandas as pd
import numpy as np
import yfinance as yf
if not hasattr(pd.Series, 'iteritems'):
    pd.Series.iteritems = pd.Series.items

class SimpleStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=20)

    def next(self):
        if not self.position:
            if self.data.close[0] > self.sma[0]:
                self.buy()
        elif self.data.close[0] < self.sma[0]:
            self.sell()


cerebro = bt.Cerebro()

data = yf.download('AAPL', start='2010-01-01', end='2021-12-31')
feed = bt.feeds.PandasData(dataname=data)
cerebro.adddata(feed)

cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(commission=0.001)

cerebro.addstrategy(SimpleStrategy)

# 使用 TimeReturn 分析器
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='time_return')

results = cerebro.run()
strat = results[0]

# 获取 TimeReturn 分析器的结果
time_return = strat.analyzers.time_return.get_analysis()

# 创建包含日期和收益率的 DataFrame
returns_df = pd.DataFrame(
    [(k, v) for k, v in time_return.items()],
    columns=['date', 'return']
).set_index('date')

# 确保索引是 DatetimeIndex 类型
returns_df.index = pd.to_datetime(returns_df.index)

# 将收益率转换为 Series
returns = returns_df['return']

# 使用 pyfolio 进行分析
pf.create_full_tear_sheet(returns)
