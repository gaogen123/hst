import backtrader as bt

from cust_indicator.主力建仓尊贵版 import 主力建仓尊贵版_indicator, get_tdx_data
from datasource.tdx_datasource import tdx_datasource


class 吸筹斜率(bt.Indicator):
    lines = ('吸筹斜率',)
    params = (
        ('period', 2),
        ('code', None),
    )

    def __init__(self):
        self.addminperiod(self.params.period)
        主力建仓尊贵版=主力建仓尊贵版_indicator(self.data, code=self.params.code)
        self.庄家线=主力建仓尊贵版.庄家线
        # self.资金线=主力建仓尊贵版.资金线

    def next(self):
        x1, x2 = 1, 2
        banker1, banker2 = self.庄家线[-1], self.庄家线[0]
        # capital1, capital2 = self.资金线[-1], self.资金线[0]
        banker_slope=(banker2 - banker1) / (x2 - x1)
        # capital_slope=(capital2 - capital1) / (x2 - x1)
        self.lines.吸筹斜率[0] = banker_slope
        # self.lines.资金斜率[0] = capital_slope
        # print(f'''
        #         日期:{self.datas[0].datetime.date(0).isoformat()}
        #         y1:{banker1}
        #         y2:{banker2}
        #         吸筹斜率:{banker_slope}
        # '''
        # )


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    code = '600084.SH'
    # dataframe = get_hst_data(code)  # 获取数据
    dataframe = get_tdx_data(code)  # 获取数据
    # df = yf.download("AAPL", start="2020-01-01", end="2021-12-31")
    # data = hst_datasource(dataname=dataframe)
    # cerebro.optstrategy(TestStrategy, code=code)
    data = tdx_datasource(dataname=dataframe)
    cerebro.adddata(data)
    # cerebro.addindicator(大盘指数,code=code)
    cerebro.addindicator(吸筹斜率, code=code)
    cerebro.broker.setcash(100000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.001)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)