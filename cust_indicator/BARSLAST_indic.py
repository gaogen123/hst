import backtrader as bt


# 上一次条件成立到当前的周期数
class BARSLAST_indic(bt.Indicator):

    lines = ('barslast',)
    params = (('VARA', None),)

    def __init__(self):
        self.count = 0
        self.VARA = self.p.VARA
    def next(self):
        # if self.condition_1[0]==1:
        #     self.count = 0
        # else:
        #     self.count += 1
        print(f"Condition value: {self.VARA[0]}")
        # self.lines.barslast[0] = self.count