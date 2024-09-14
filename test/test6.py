import json
import requests
from MyTT import *
from 筹码分布 import ChipDistribution



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


import backtrader as bt


class PandasSMA(bt.Indicator):
    lines = ('控盘','无庄控盘','开始控盘', '有庄控盘', '高度控盘','主力出货')

    params = (
        ('period', 10),
    )

    def __init__(self):
        a = ChipDistribution()
        a.data['close']=pd.Series(self.data.close.array,name='close').astype(float)
        # a.data['TurnoverRate']=pd.Series(self.data.TurnoverRate.array).astype(float)
        a.data['volume']=pd.Series(self.data.volume.array).astype(int)
        a.data['open']=pd.Series(self.data.open.array).astype(float)
        a.data['high']=pd.Series(self.data.high.array).astype(float)
        a.data['low']=pd.Series(self.data.low.array).astype(float)
        a.data['close']=pd.Series(self.data.close.array).astype(float)
        # a.data['money']=a.data['volume']*a.data['close'].astype(float)
        # a.data['avg']=a.data['money'].astype(float)/a.data['volume'].astype(int)
        VAR1 = EMA(EMA(self.data.close.array, 9), 9)
        self.控盘 = (VAR1 - REF(VAR1, 1)) / REF(VAR1, 1) * 1000
        # STICKLINE(self.控盘<0,self.控盘,0,cust_indicator,0),COLORWHITE;
        A10 = CROSS(self.控盘, 0)
        self.无庄控盘 = IF(self.控盘 < 0, self.控盘, 0)
        # self.开始控盘 = IF(A10, 5, 0)
        # self.有庄控盘 = IF((self.控盘 > REF(self.控盘, cust_indicator)) & (self.控盘 > 0), self.控盘, 0)
        # a.calcuChip(flag=cust_indicator, AC=cust_indicator)  # 计算
        # 成本分布 = np.asarray(a.cost(85))  # 成本分布
        # VAR2 = np.asarray(a.winner()) * 100
        # self.高度控盘 = IF((VAR2 > 50) & (成本分布 < np.asarray(self.data.close.array)) & (控盘 > 0), 控盘, 0)
        self.主力出货 = IF((self.控盘 < REF(self.控盘, 1)) & (self.控盘 > 0), self.控盘, 0)

    def next(self):
        self.lines.控盘[0] = self.控盘[len(self.控盘) - 1]
        self.lines.无庄控盘[0] = self.无庄控盘[len(self.无庄控盘) - 1]
        # self.lines.开始控盘[0] = self.开始控盘[len(self.开始控盘) - cust_indicator]
        # self.lines.有庄控盘[0] = self.有庄控盘[len(self.有庄控盘) - cust_indicator]
        # self.lines.高度控盘[0] = self.高度控盘[len(self.高度控盘) - cust_indicator]
        # self.lines.主力出货[0] = self.主力出货[len(self.主力出货) - cust_indicator]
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
        ('printlog', False),
        ('dataframe', None),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.控盘 = PandasSMA(self.data, period=10)

    def next(self):
        print(self.控盘[0])


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))




    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)

if __name__ == '__main__':
    code='02439.HK'
    dataframe=get_data(code)
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    # Add a strategy
    # Add a strategy
    strats = cerebro.optstrategy(
        TestStrategy,
        maperiod=range(10, 31),dataframe=dataframe)



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
