import backtrader as bt

from cust_indicator.主力建仓尊贵版 import 主力建仓尊贵版_indicator, get_tdx_data
from cust_indicator.黄金坑稳赚买 import 黄金坑稳赚买_indicator
from datasource.tdx_datasource import tdx_datasource


class 黄金坑2日斜率_indc(bt.Indicator):
    lines = ('黄金坑斜率_line',)
    params = (
        ('code', None),
    )

    def __init__(self):
        黄金坑稳赚买 = 黄金坑稳赚买_indicator(self.data, code=self.params.code)
        # self.庄家线=主力建仓尊贵版.庄家线
        self.黄金坑=黄金坑稳赚买.黄金坑_line
        hjk1=self.黄金坑(-1)
        hjk2 = self.黄金坑(0)
        self.hjk_slope = (hjk2 - hjk1)/1
        self.lines.黄金坑斜率_line=self.hjk_slope

    # def next(self):
        # x1, x2 = 1, 2
        # hjk1, hjk2 = self.黄金坑[-1], self.黄金坑[0]
        # hjk_slope=(hjk2 - hjk1) / (x2 - x1)
        # self.lines.黄金坑斜率[0] = hjk_slope
        # print(f'''
        #         日期:{self.datas[0].datetime.date(0).isoformat()}
        #         hjk1:{hjk1}
        #         hjk2:{hjk2}
        #         黄金坑:{self.黄金坑[0]}
        #         黄金坑斜率:{hjk_slope}
        # '''
        # )
        # print(f'''
        #                日期:{self.datas[0].datetime.date(0).isoformat()}
        #                hjk_slope:{self.hjk_slope[0]}
        #        '''
        #       )


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
    cerebro.addindicator(资金斜率, code=code)
    cerebro.broker.setcash(100000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.001)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)