import backtrader as bt

class COUNT_indicator(bt.Indicator):
    lines = ('count',)
    params = (('condition', None), ('period', 0))

    def __init__(self):
        self.addminperiod(self.p.period)
        self.condition = self.p.condition

    def next(self):
        if self.p.period == 0:
            # 如果没有指定周期，计算所有历史数据中满足条件的次数
            self.lines.count[0] = sum(1 for i in range(len(self)) if self.condition[i])
        else:
            # 如果指定了周期，只计算最近period个周期内满足条件的次数
            self.lines.count[0] = sum(1 for i in range(max(0, len(self) - self.p.period), len(self)) if self.condition[i])