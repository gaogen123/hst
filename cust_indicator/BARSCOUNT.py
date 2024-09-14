import backtrader as bt

class BARSCOUNT(bt.Indicator):
    lines = ('count',)
    params = (('condition', None),)

    def __init__(self):
        self.count = 0
        self.condition = self.params.condition

    def next(self):
        if self.condition is not None and self.condition[0]:
            self.count += 1
        # else:
        #     self.count = 0
        
        self.lines.count[0] = self.count