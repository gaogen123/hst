import backtrader as bt
class TurnoverRate(bt.Indicator):
    lines = ('turnover',)  # 定义输出线
    params = (
        ('circulating_capital', None),  # 流通股本，默认需要从外部传入
    )

    def __init__(self):
        super().__init__()
        if self.params.circulating_capital is None:
            raise ValueError("必须提供流通股本(circulating_capital)参数")

    def next(self):
        # 确保流通股本不为0以避免除零错误
        if self.params.circulating_capital > 0:
            self.lines.turnover[0] = (self.data.volume[0] / self.params.circulating_capital) * 100
        else:
            self.lines.turnover[0] = 0.0  # 或者根据需要处理这种情况