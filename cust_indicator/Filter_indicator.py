import backtrader as bt

class Filter_indicator(bt.Indicator):
    lines = ('filtered',)
    params = (('period', 5),('condition', None),)

    def __init__(self):
        self.condition = self.params.condition
        self.count = 0

    def next(self):
        if self.count > 0:
            self.count -= 1
            self.lines.filtered[0] = 0
        elif self.condition[0]:
            self.lines.filtered[0] = 1
            self.count = self.p.period - 1
        else:
            self.lines.filtered[0] = 0