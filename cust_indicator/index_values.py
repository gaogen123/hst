import backtrader as bt
import baostock as bs
import pandas as pd
import akshare as ak  # 添加此行以导入 akshare 库
class index_values(bt.Indicator):
    lines = ('index_close','index_low','index_high',)
    params = (
        ('code', None),
    )
    def __init__(self):
        self.code=self.params.code
        bs.login()
    def next(self):

        code1 = self.code.split('.')[0]
        # 上证
        if code1.startswith('600') or code1.startswith('601') or code1.startswith('603') or code1.startswith('605'):
            index_code = 'sh000001'
        # 深证
        if code1.startswith('000') or code1.startswith('200'):
            index_code = 'sz399001'
        # 创业板
        if code1.startswith('300'):
            index_code = 'sz399006'
        start_date = self.data.datetime.date(0).isoformat()
        end_date = self.data.datetime.date(0).isoformat()
        index_data = ak.stock_zh_index_daily(symbol=index_code)
        index_data['date'] = pd.to_datetime(index_data['date']).dt.date  # 将日期转换为 datetime.date 类型
        index_data = index_data[(index_data['date'] >= pd.to_datetime(start_date).date()) & (index_data['date'] <= pd.to_datetime(end_date).date())]

        self.lines.index_close[0] = float(index_data['close'].values[0])
        self.lines.index_low[0] = float(index_data['low'].values[0])
        self.lines.index_high[0] = float(index_data['high'].values[0])