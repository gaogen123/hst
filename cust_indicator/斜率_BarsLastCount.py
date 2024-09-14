import backtrader as bt

from cust_indicator.吸筹斜率 import 吸筹斜率
from cust_indicator.资金斜率 import 资金斜率


class 斜率_BarsLastCount(bt.Indicator):
    lines = ('资金斜率_count','吸筹斜率_count',)
    params = (('code', None),)

    def __init__(self):
        self.资金_斜率 = 资金斜率(self.data, code=self.params.code).资金斜率
        self.吸筹_斜率 = 吸筹斜率(self.data, code=self.params.code).吸筹斜率
        self.addminperiod(1)
        self.资金_count = 0
        self.吸筹_count = 0

    def next(self):
        if self.资金_斜率[-1]<0:
            self.资金_count += 1
        else:
            self.资金_count = 0

        if self.吸筹_斜率[-1]>0:
            self.吸筹_count += 1
        else:
            self.吸筹_count = 0

        self.lines.资金斜率_count[0] = self.资金_count
        self.lines.吸筹斜率_count[0] = self.吸筹_count
        # print(
        #     f'''
        #     日期:{self.datas[0].datetime.date(0).isoformat()}
        #     资金_斜率:{self.资金_斜率[0]}
        #     上一日资金_斜率:{self.资金_斜率[-1]}
        #     资金_count:{self.资金_count}
        #     吸筹_斜率:{self.吸筹_斜率[0]}
        #     上一日吸筹_斜率:{self.吸筹_斜率[-1]}
        #     吸筹_count:{self.吸筹_count}
        #     '''
        # )