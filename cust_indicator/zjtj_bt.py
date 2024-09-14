from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import json
import backtrader as bt
import backtrader.indicators as btind
import pandas as pd
import requests

from cust_indicator.chipDistribution_indicator import chipDistribution_indicator
from datasource.hst_datasource import tdx_datasource




def get_data(code):
    url = 'http://127.0.0.1:11111/hq/KL'
    kw = {
        "timeout_sec": 10,
        "params": {
            "security": {
                "dataType": "30000",
                "code": code
            },
            "startDate": "20240101",
            "direction": "1",
            "exRightFlag": "0",
            "cycType": "2",
            "limit": "500"
        }
    }
    json_str = json.dumps(kw)
    response = requests.post(url, data=json_str)
    pd_data=pd.read_json(json.dumps(json.loads(response.text)['data']['kline']))

    pd_data=pd_data.set_index('date',drop=False)
    # pd_data=pd_data.set_index('date',drop=False).rename(columns={'closePrice': 'close', 'highPrice': 'high', 'openPrice': 'open', 'volume': 'volume','lowPrice':'low'})
    return pd_data

class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 10),
        ('printlog', False),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

        self.ema_one = bt.indicators.EMA(self.datas[0].close, period=9)
        self.VAR1 = bt.indicators.EMA(self.ema_one, period=9)
        self.控盘 = (self.VAR1 - self.VAR1(-1)) / self.VAR1(-1) * 1000
        self.A10=btind.CrossOver(self.控盘, 0)
        self.无庄控盘 = bt.If(self.控盘 < 0, self.控盘, 0)
        self.开始控盘 = bt.If(self.A10>0, 5, 0)
        self.有庄控盘 = bt.If(bt.And((self.控盘 > self.控盘(-1)),(self.控盘 > 0)) , self.控盘, 0)
        # self.minimum_period = 20
        self.筹码分布 = chipDistribution_indicator(self.data,cost_pct=85)
        self.成本分布 =  self.筹码分布.cost_line  # 成本分布
        self.VAR2=self.筹码分布.winner_line*100
        self.高度控盘=bt.If(bt.And(self.VAR2>50,self.成本分布<self.datas[0].close,self.控盘>0),self.控盘,0)
        self.主力出货=bt.If(bt.And(self.控盘<self.控盘(-1),self.控盘>0),self.控盘,0)


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


    def next(self):
        print(f'''
                       日期:{self.datas[0].datetime.date(0).isoformat()}
                       ,控盘:{self.控盘[0]}
                       ,A10:{self.A10[0]}
                       ,无庄控盘:{self.无庄控盘[0]}
                       ,开始控盘:{self.开始控盘[0]}
                       ,有庄控盘:{self.有庄控盘[0]}
                       ,筹码分布:{self.筹码分布.cost_line[0]}
                       ,VAR2:{self.VAR2[0]}
                       ,高度控盘:{self.高度控盘[0]}
                       ,主力出货:{self.主力出货[0]}
                   ''')
        # 控盘 = (self.VAR1[0]-self.VAR1[-1])/ self.VAR1[-1] *1000
        # ref_VAR1=self.VAR1.data[-1]
        # # A10 = btind.CrossOver(控盘, 0)
        # print(f'''
        #             日期:{self.datas[0].datetime.date(0).isoformat()}
        #             EMA:{self.ema_one[0]}
        #             ,VAR1:{self.VAR1[0]}
        #             ,ref_VAR1:{ref_VAR1}
        #             ,相减:{self.VAR1[0]-ref_VAR1}
        #             ,控盘:{控盘}
        #         ''')
        # STICKLINE(控盘<0,控盘,0,cust_indicator,0),COLORWHITE;
        # A10 = self.CROSS(控盘, 0)
        # 无庄控盘 = IF(控盘 < 0, 控盘, 0)
        # 开始控盘 = IF(A10, 5, 0)
        # # STICKLINE(控盘>REF(控盘,cust_indicator) AND 控盘>0,控盘,0,cust_indicator,0),COLORRED;
        # 有庄控盘 = IF((控盘 > REF(控盘, cust_indicator)) & (控盘 > 0), 控盘, 0)
        # # VAR2:=100*WINNER(CLOSE*0.95);
        # a.calcuChip(flag=cust_indicator, AC=cust_indicator)  # 计算
        # 成本分布 = np.asarray(a.cost(85))  # 成本分布
        # VAR2 = np.asarray(a.winner()) * 100
        #
        # close = df.close.values
        # # STICKLINE(VAR2>50 AND COST(85)<CLOSE AND 控盘>0,控盘,0,cust_indicator,0),COLORFF00FF;
        # # 高度控盘:IF(VAR2>50 AND COST(85)<CLOSE AND 控盘>0,控盘,0),COLORFF00FF,NODRAW;
        # 高度控盘 = IF((VAR2 > 50) & (成本分布 < df.close.values) & (控盘 > 0), 控盘, 0)
        # # STICKLINE(控盘<REF(控盘,cust_indicator) AND 控盘>0,控盘,0,cust_indicator,0),COLOR00FF00;
        # 主力出货 = IF((控盘 < REF(控盘, cust_indicator)) & (控盘 > 0), 控盘, 0)
        # # print(主力出货)
        # # 设置主题和颜色调色板
        # sns.set_theme(style="darkgrid", palette="pastel")
        # # 创建柱状图
        # sns.barplot(x=df['date'], y=开始控盘, )
        # # 显示图表
        # plt.show()















        #
        # # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])
        #
        # # Check if an order is pending ... if yes, we cannot send a 2nd one
        # if self.order:
        #     return
        #
        # # Check if we are in the market
        # if not self.position:
        #
        #     # Not yet ... we MIGHT BUY if ...
        #     if self.dataclose[0] > self.sma[0]:
        #
        #         # BUY, BUY, BUY!!! (with all possible default parameters)
        #         self.log('BUY CREATE, %.2f' % self.dataclose[0])
        #
        #         # Keep track of the created order to avoid a 2nd order
        #         self.order = self.buy()
        #
        # else:
        #
        #     if self.dataclose[0] < self.sma[0]:
        #         # SELL, SELL, SELL!!! (with all possible default parameters)
        #         self.log('SELL CREATE, %.2f' % self.dataclose[0])
        #
        #         # Keep track of the created order to avoid a 2nd order
        #         self.order = self.sell()

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    strats = cerebro.optstrategy(
        TestStrategy)
    code='601398.SH'
    dataframe=get_data(code)# 获取数据
    # df = yf.download("AAPL", start="2020-01-01", end="2021-12-31")
    data=tdx_datasource(dataname=dataframe)
    # data = bt.feeds.PandasData(dataname=dataframe)
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.001)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)
