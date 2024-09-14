import backtrader as bt
import numpy as np

class VAVEDEV_Indicator(bt.Indicator):
    lines = ('vavedev',)
    params = (('period', 10),('price', None),)

    def __init__(self):
        self.addminperiod(self.params.period)

    def next(self):
        volume_array = np.array(self.price.get(size=self.params.period))
        mean_volume = np.mean(volume_array)
        absolute_deviation = np.abs(volume_array - mean_volume)
        self.lines.vavedev[0] = np.mean(absolute_deviation)