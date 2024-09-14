import backtrader as bt
import json
import requests
from MyTT import *


class DualMAIndicator(bt.Indicator):
    lines = ('short_ma', 'long_ma', 'ma_diff','test')  # 定义三个输出线

    params = (
        ('short_period', 15),  # 短期移动平均线周期
        ('long_period', 50),  # 长期移动平均线周期
    )
    def get_cost(self):
        self.data



    def __init__(self):
        # 添加最小周期检查
        self.addminperiod(max(self.params.short_period, self.params.long_period))

        # 计算短期和长期移动平均线
        self.lines.short_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
        self.lines.long_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)

        # 计算两者的差值
        self.lines.ma_diff = self.lines.short_ma - self.lines.long_ma
        self.lines.test = bt.LineSeries(EMA(EMA(self.data.close.array, 9), 9),name='test')



# 定义策略
class TestStrategy(bt.Strategy):
    def __init__(self):
        # 实例化自定义指标
        self.dual_ma = DualMAIndicator(self.data)

    def next(self):
        print(f'Date: {self.data.datetime.date(0)}, Close: {self.data.close[0]}, '
              f'Short MA: {self.dual_ma.short_ma[0]}, Long MA: {self.dual_ma.long_ma[0]}, '
              f'Diff: {self.dual_ma.ma_diff[0]} ,'
              f'test: {self.dual_ma.test[0]} ,'
              )

def get_data(code):
    url = 'http://127.0.0.1:11111/hq/KL'
    kw = {
        "timeout_sec": 10,
        "params": {
            "security": {
                "dataType": "10000",
                "code": code
            },
            "startDate": "20240101",
            "direction": "cust_indicator",
            "exRightFlag": "2",
            "cycType": "2",
            "limit": "500"
        }
    }
    json_str = json.dumps(kw)
    response = requests.post(url, data=json_str)
    return pd.read_json(json.dumps(json.loads(response.text)['data']['kline'])).set_index('date').rename(columns={'closePrice': 'close', 'highPrice': 'high', 'openPrice': 'open', 'volume': 'volume','lowPrice': 'low','turnover': 'TurnoverRate'})


code = '02439.HK'
dataframe = get_data(code)
# Create a cerebro entity
cerebro = bt.Cerebro()
# Add a strategy
# Add a strategy
strats = cerebro.optstrategy(
    TestStrategy)

data = bt.feeds.PandasData(dataname=dataframe)
cerebro.adddata(data)
# Set our desired cash start
cerebro.broker.setcash(100000.0)
# Add a FixedSize sizer according to the stake
cerebro.addsizer(bt.sizers.FixedSize, stake=10)
# Set the commission - 0.cust_indicator% ... divide by 100 to remove the %
cerebro.broker.setcommission(commission=0.001)

# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Run over everything
cerebro.run(maxcpus=1)