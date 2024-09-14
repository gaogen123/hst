import backtrader as bt
import yfinance as yf
import pandas as pd

class MultiStockStrategy(bt.Strategy):
    def __init__(self):
        self.sma = {data: bt.indicators.SimpleMovingAverage(data, period=20) for data in self.datas}

    def next(self):
        for data in self.datas:
            if not self.position:
                if data.close[0] > self.sma[data][0]:
                    self.buy(data)
            else:
                if data.close[0] < self.sma[data][0]:
                    self.sell(data)

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # 股票列表
    stocks = ['AAPL', 'GOOGL', 'MSFT']

    # 获取数据并添加到Cerebro
    for stock in stocks:
        data = bt.feeds.PandasData(dataname=yf.download(stock, '2020-01-01', '2021-12-31'))
        cerebro.adddata(data, name=stock)

    # 设置初始资金
    cerebro.broker.setcash(100000.0)

    # 添加策略
    cerebro.addstrategy(MultiStockStrategy)

    cerebro.run()
