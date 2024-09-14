import backtrader as bt
#todo 待优化 放到init里面
class CustomEMA(bt.Indicator):
    lines = ('sma',)
    params = (('period', 20), ('weight', 1))

    def __init__(self):
        self.y_prev=0

    def next(self):
        x = self.data[0]
        n = self.params.period
        m = self.params.weight

        self.y_prev= (x * m + self.y_prev * (n - m)) / n
        self.lines.sma[0] =self.y_prev