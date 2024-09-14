import time
import json
import datetime

import backtrader as bt
import requests


class RealtimeData(bt.feed.DataBase):
    '''
    实时数据源
    '''

    # 需要定义的一些线
    lines = ('datetime', 'open', 'high', 'low', 'close', 'volume', 'openinterest')

    # 参数列表，包括数据源的一些配置信息
    params = (
        ('symbol', ''),  # 交易对符号
        ('api_url', ''),  # API 地址
        ('backfill_start', None),  # 回填数据的起始时间
        ('backfill_end', None),  # 回填数据的结束时间
        ('param', {
            "timeout_sec": 10,
            "params": {
                "security": [{
                    "dataType": "20000",
                    "code": "TNXP"
                }],
                "needDelayFlag": "cust_indicator",
                "mktTmType": "-cust_indicator"
            }
        })
    )
    def islive(self):
        return True

    def start(self):
        # 如果设置了回填数据的起始时间和结束时间，则先回填历史数据
        if self.p.backfill_start and self.p.backfill_end:
            self.backfill_data()



    def backfill_data(self):
        # 从 API 获取历史数据并添加到数据源中
        # ...
        pass

    def next(self):

        # 持续从 API 获取实时数据并添加到数据源中
        while True:
            # 从 API 获取最新的行情数据
            response = requests.post(self.params.api_url, data=json.dumps(self.params.param))
            data = response.json()

            # 创建一个新的 bar 对象并添加到数据源中
            # self.lines.datetime[0] = time.time()
            self.lines.open[0] = data['data']['basicQot'][0]['openPrice']
            self.lines.high[0] = data['data']['basicQot'][0]['highPrice']
            self.lines.low[0] = data['data']['basicQot'][0]['lowPrice']
            self.lines.close[0] = data['data']['basicQot'][0]['lastPrice']
            self.lines.volume[0] = data['data']['basicQot'][0]['volume']


            # 等待一段时间后再获取下一个 bar
            time.sleep(60)  # 假设每 60 秒获取一次新数据

class TestStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=5)

    def next(self):
        print(f'Date: {self.data.datetime.datetime(0)}, Close: {self.data.close[0]}, SMA: {self.sma[0]}')


import backtrader as bt

# 创建一个 Cerebro 实例
cerebro = bt.Cerebro()

# 添加自定义的实时数据源
data = RealtimeData(
    symbol='BTC-USD',
    api_url='http://127.0.0.1:11111/hq/BasicQot',
    backfill_start=datetime.datetime(2022, 1, 1),
    backfill_end=datetime.datetime(2022, 1, 31)
)
cerebro.adddata(data)
# 添加策略
cerebro.addstrategy(TestStrategy)


# 运行回测
cerebro.run()
