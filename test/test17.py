import backtrader as bt
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams
import pandas as pd
from datetime import datetime
import time


# 获取上证股票列表
def get_sse_stocks():
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        stocks = api.get_security_list(1, 0)
    return [s['code'] for s in stocks if s['code'][0] == '6']


# 获取股票数据
def get_stock_data(code, start_date, end_date):
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        data = []
        start_date = int(start_date)
        end_date = int(end_date)
        for i in range(10):  # 最多获取10个1000条数据块
            tmp_data = api.get_security_bars(9, 1, code, (9 - i) * 800, 800)
            if not tmp_data:
                break
            data += tmp_data
            if tmp_data[0]['datetime'] <= start_date:
                break

    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df[(df['datetime'] >= pd.Timestamp(start_date)) & (df['datetime'] <= pd.Timestamp(end_date))]
    df = df.rename(columns={
        'datetime': 'date', 'open': 'open', 'high': 'high', 'low': 'low',
        'close': 'close', 'vol': 'volume', 'amount': 'openinterest'
    })
    df = df.set_index('date')
    df = df.sort_index()
    return df


# 定义策略（与之前相同）
class MyStrategy(bt.Strategy):
    params = (('sma_period', 20),)

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_period)

    def next(self):
        if not self.position:
            if self.data.close[0] > self.sma[0]:
                self.buy()
        else:
            if self.data.close[0] < self.sma[0]:
                self.sell()


# 运行回测
def run_backtest(stock_code, start_date, end_date):
    cerebro = bt.Cerebro()

    # 获取数据
    data = get_stock_data(stock_code, start_date, end_date)
    feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(feed)

    # 设置初始资金
    cerebro.broker.setcash(100000.0)

    # 添加策略
    cerebro.addstrategy(MyStrategy)

    # 运行回测
    initial_value = cerebro.broker.getvalue()
    results = cerebro.run()
    final_value = cerebro.broker.getvalue()

    return (stock_code, initial_value, final_value)


# 主程序
if __name__ == '__main__':
    start_date = '20200101'
    end_date = '20211231'

    # 获取上证股票列表
    sse_stocks = get_sse_stocks()

    # 运行回测
    results = []
    for stock in sse_stocks:
        try:
            result = run_backtest(stock, start_date, end_date)
            results.append(result)
            print(f"Completed backtest for {stock}")
        except Exception as e:
            print(f"Error in backtest for {stock}: {e}")
        time.sleep(1)  # 添加延迟以避免请求过于频繁

    # 输出结果
    results_df = pd.DataFrame(results, columns=['Stock', 'Initial Value', 'Final Value'])
    results_df['Return'] = (results_df['Final Value'] - results_df['Initial Value']) / results_df['Initial Value']
    results_df = results_df.sort_values('Return', ascending=False)
    print(results_df)

    # 保存结果
    results_df.to_csv('backtest_results.csv', index=False)
