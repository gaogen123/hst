import json

import backtrader as bt
import requests
import time
from datetime import datetime, timedelta


class RealTimeData(bt.feed.DataBase):
    params = (
        ('url', 'http://127.0.0.1:11111/hq/BasicQot'),  # HTTP请求的URL
        ('poll_interval', 10),  # 请求间隔时间（秒）
        ('data', {
            "timeout_sec": 10,
            "params": {
                "security": [{
                    "dataType": "20000",
                    "code": "TNXP"
                }],
                "needDelayFlag": "cust_indicator",
                "mktTmType": "-cust_indicator"
            }
        }),
    )
    def islive(self):
        return True


    def __init__(self):
        self.next_poll = datetime.now()

    def start(self):
        super(RealTimeData, self).start()
        self.lastupdate = datetime.min
        self.data = None

    def stop(self):
        super(RealTimeData, self).stop()

    def _load(self):
        if datetime.now() >= self.next_poll:
            self.next_poll = datetime.now() + timedelta(seconds=self.params.poll_interval)
            response = requests.post(self.params.url,data=json.dumps(self.params.data))
            if response.status_code == 200:
                data = response.json()
                self.data = data
                self.lastupdate = datetime.now()

        if self.data:
            # self.lines.datetime[0] = time.time()
            trade_time=datetime.strptime(self.data['data']['basicQot'][0]['tradeTime'], '%Y%m%d%H%M%S')
            day=trade_time.day
            hours = trade_time.hour
            minutes = trade_time.minute
            total_minutes = hours * 60 + minutes
            days = total_minutes / (24 * 60)
            finally_day=day+days
            self.lines.datetime[0]=finally_day
            self.lines.open[0] = self.data['data']['basicQot'][0]['openPrice']
            self.lines.high[0] = self.data['data']['basicQot'][0]['highPrice']
            self.lines.low[0] = self.data['data']['basicQot'][0]['lowPrice']
            self.lines.close[0] = self.data['data']['basicQot'][0]['lastPrice']
            self.lines.volume[0] = self.data['data']['basicQot'][0]['volume']
            return True
        else:
            return False


# 示例策略
class TestStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=5)

    def next(self):
        print(f'Close: {self.data.close[0]}')


# 初始化Cerebro引擎
cerebro = bt.Cerebro()

# 添加自定义实时数据源
data = RealTimeData(url='http://127.0.0.1:11111/hq/BasicQot', poll_interval=10)
cerebro.adddata(data)

# 添加策略
cerebro.addstrategy(TestStrategy)

# 运行回测
cerebro.run()