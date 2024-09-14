import akshare as ak
import backtrader as bt
# from my_tool import *
import pandas as pd
from backtrader.indicators import CrossUp, CrossDown
from pytdx.hq import TdxHq_API

from cust_indicator.BARSCOUNT import BARSCOUNT
from cust_indicator.CustomEMA import CustomEMA
from cust_indicator.chipDistribution_indicator import chipDistribution_indicator
from datasource.akshare_datasource import akshare_datasource
from 筹码分布 import ChipDistribution

#获取btc.usdt交易对120日的数据
# df=get_price('btc.usdt',count=120,frequency='1d');     #'1d'是1天, '4h'是4小时
# a = ChipDistribution()
# code = 'sh.600084'
# start_date='2023-05-25'
# end_date='2024-05-31'
# a.get_data(code,start_date, end_date)  #获取数据
# a.calcuChip(flag=1, AC=1) #计算
# a.get_data(code, start_date, end_date)  # 获取数据
# df=a.data
#流通股本
# CAPITAL= float(my_fun.get_net_profit(code,year=2024, quarter=1))


def get_tdx_data(code='000001'):
    code_1=code.split('.')[0]
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        data = api.to_df(api.get_security_bars(9, 1, code_1, 0, 500))  # 返回DataFrame
    tdx_liutongguben = get_tdx_liutongguben(code_1)
    data['hsl']=data['vol']/tdx_liutongguben if tdx_liutongguben>0 else 0
    data['datetime'] = pd.to_datetime(data['datetime'])
    data['code'] = int(code_1)
    return data
def get_tdx_liutongguben(code):
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        data = api.to_df(api.get_finance_info(1, code))  # 返回DataFrame
    return data['liutongguben'][0]


class TestStrategy(bt.Strategy):
    params = (
        ('code', None),
    )

    def __init__(self):
        # code = self.params.code
        # self.主力建仓尊贵版_indicator = 主力建仓尊贵版_indicator(self.data,code=code)
        pass

class 黄金坑稳赚买_indicator(bt.Indicator):

    lines = (
        '黄金坑_line',
        '稳赚买_line',
        '财神到_line',
        '春笋_line',
        '买_line',
    )
    params = (
        ('code', None),
    )

    def __init__(self):
        try:
            筹码分布 = chipDistribution_indicator(self.data)
            self.winner_line = 筹码分布.winner_line
            self.VAR1 = bt.indicators.MovingAverageSimple(筹码分布.winner_line, period=9) * 100

            self.买 = CrossUp(self.VAR1, 2) * 30
            # self.high_colse=bt.indicators.Highest(self.datas[0].high, period=15) - self.datas[0].close
            self.VAR2=bt.If(
                                bt.indicators.Highest(self.datas[0].high, period=15) - bt.indicators.Lowest(self.datas[0].low,period=15)!=0
                                ,(1 - bt.indicators.EMA((bt.indicators.Highest(self.datas[0].high, period=15) - self.datas[0].close) /(bt.indicators.Highest(self.datas[0].high, period=15) - bt.indicators.Lowest(self.datas[0].low,period=15)), period=15)) * 100
                                ,0
                            )
            VAR3 =bt.If(bt.indicators.Highest(self.datas[0].high, period=21) - bt.indicators.Lowest(self.datas[0].low,period=21)!=0
                  ,(self.datas[0].close - bt.indicators.Lowest(self.datas[0].low, period=21)) / (bt.indicators.Highest(self.datas[0].high, period=21) - bt.indicators.Lowest(self.datas[0].low,period=21)) * 100
                  ,0
                  )
            VAR4 = CustomEMA(VAR3, period=9, weight=1);
            VAR5 = CustomEMA(VAR4, period=9, weight=1);
            VAR6 = bt.If(
                    CustomEMA(self.datas[0].close, period=13, weight=1)!=0
                    ,(self.datas[0].close - CustomEMA(self.datas[0].close, period=13, weight=1)) / CustomEMA(self.datas[0].close, period=13, weight=1) * (-100)
                    ,0
                )
            VAR7 =bt.If(bt.And(VAR6!=0,self.datas[0].close(-1)!=0)
                  ,bt.And(VAR6(-1) > 13, VAR6(-1) / VAR6 > 1.23, self.datas[0].close / self.datas[0].close(-1) > 1.03)
                  ,0
                  )
            筹码分布_5 = chipDistribution_indicator(self.data, cost_pct=5)
            self.春笋 = bt.If(bt.And(VAR7 > 0, self.datas[0].close(-1) <= 筹码分布_5.cost_line), 20, 0)
            VAR8 = bt.indicators.MovingAverageSimple(self.datas[0].close, period=27);
            VAR9 =bt.If(  VAR8!=0
                  ,(self.datas[0].close - VAR8) / VAR8 * 100
                  ,0
                )
            self.VARA = bt.indicators.MovingAverageSimple(VAR9, period=2);
            # # self.VAR17 = BARSCOUNT(condition=self.datas[0].close != None)
            self.VARA_Cross = CrossDown(self.VARA, -10)
            self.VARA_Cross_bool = bt.And(self.VARA_Cross == 1)
            self.VARB = 黄金坑稳赚稳买_VAR(self.data).VARB
            self.VARC = 黄金坑稳赚稳买_VAR(self.data).VARC
            self.VARD = bt.And(self.VARA < -10, self.VARB > 3);
            VARE = bt.And(self.VARA > 10, self.VARC > 3);
            self.黄金坑 = bt.If(self.VARD, self.VARA, 0);
            self.财神到 = bt.If(VARE, self.VARA, 0)
            self.稳赚买 = bt.If(bt.And(self.VARA > self.VARA(-1), self.VARD == 1, self.VARA < -15), 30, 0)

            # DRAWICON(稳赚买>0,40,cust_indicator);
            VARF = self.datas[0].low(-1) * 0.9;
            VAR10 = self.datas[0].low * 0.9;
            # VAR11 = bt.If(CAPITAL!=0,(VAR10 * self.datas[0].volume + VARF * (CAPITAL - self.datas[0].volume)) / CAPITAL,0)
            # VAR12 = bt.indicators.EMA(VAR11, period=30);
            VAR13 = self.datas[0].close - self.datas[0].close(-1);
            VAR14 = bt.Max(VAR13, 0);
            VAR15 = abs(VAR13);
            VAR16 =bt.If(
                CustomEMA(VAR15, period=7, weight=1)!=0
                , CustomEMA(VAR14, period=7, weight=1) / CustomEMA(VAR15, period=7, weight=1) * 100
                ,0
            )
            VAR17 =bt.If(
                CustomEMA(VAR15, period=13, weight=1)!=0
                ,CustomEMA(VAR14, period=13, weight=1) / CustomEMA(VAR15, period=13, weight=1) * 100
                ,0
            )
            VAR18 = BARSCOUNT(condition=self.datas[0].close);
            VAR19 =bt.If(
                    CustomEMA(abs(VAR13), period=16, weight=1)!=0
                    ,CustomEMA(bt.Max(VAR13, 0), period=16, weight=1) / CustomEMA(abs(VAR13), period=16, weight=1) * 100
                    ,0
                  )
            VAR1A = (-200) * (bt.indicators.Highest(self.datas[0].high, period=60) - self.datas[0].close) / (
                    bt.indicators.Highest(self.datas[0].high, period=60) - bt.indicators.Lowest(self.datas[0].low,period=60)) + 100;
            VAR1B =bt.If(
                bt.indicators.Highest(self.datas[0].high, period=15) - bt.indicators.Lowest(self.datas[0].low,period=15)!=0
                ,(self.datas[0].close - bt.indicators.Lowest(self.datas[0].low, period=15)) / ( bt.indicators.Highest(self.datas[0].high, period=15) - bt.indicators.Lowest(self.datas[0].low, period=15)) * 100
                ,0
            )
            VAR1C = CustomEMA((CustomEMA(VAR1B, period=4, weight=1) - 50) * 2, period=3, weight=1);
            # self.INDEXC = index_values(self.data, code=self.params.code).index_close
            # INDEXL = index_values(self.data, code=self.params.code).index_low
            # INDEXH = index_values(self.data, code=self.params.code).index_high
            # self.VAR1D = (self.INDEXC - bt.indicators.Lowest(INDEXL, period=14)) / (bt.indicators.Highest(INDEXH, period=14) - bt.indicators.Lowest(INDEXL, period=14)) * 100;
            # VAR1E = CustomEMA(self.VAR1D, period=4, weight=1);
            # self.VAR1F = CustomEMA(VAR1E, period=3, weight=1);
            # self.VAR20 = (bt.indicators.Highest(self.datas[0].high, period=30) - self.datas[0].close) / self.datas[0].close * 100;
            # VAR21 = bt.And(VAR19 <= 25, (VAR1A < -95) , (self.VAR20 > 20) , (VAR1C < -30) , (self.VAR1F < 30) , (
            #             VAR12 - self.datas[0].close >= -0.25) , (VAR16 < 22) , (VAR17 < 28) , (VAR18 > 50));
            # self.超跌 = VAR21

            self.lines.黄金坑_line = self.黄金坑
            self.lines.稳赚买_line = self.稳赚买
            self.lines.财神到_line = self.财神到
            self.lines.春笋_line = self.春笋
            self.lines.买_line = self.买


        except ZeroDivisionError as e:
            self.log.error(f"初始化过程中发生除零错误: {e}")
            # 处理错误,可能设置默认值或者标记策略为无效
        except Exception as e:
            self.log(f"初始化过程中发生未知错误: {e}")
            # 处理其他类型的错误




    # def next(self):
    #     print(f'''
    #      日期:{self.datas[0].datetime.date(0).isoformat()}
    #      黄金坑:{self.黄金坑[0]}
    #      春笋:{self.春笋[0]}
    #      买:{self.买[0]}
    #      财神到:{self.财神到[0]}
    #      稳赚买:{self.稳赚买[0]}
    #      超跌:{self.超跌[0]}
    #                    ''')

class 黄金坑稳赚稳买_VAR(bt.Indicator):
    lines = ('VARB','VARC',)

    def __init__(self):
        self.varb_count = 0
        self.varc_count = 0
        VAR8 = bt.indicators.MovingAverageSimple(self.datas[0].close, period=27);
        VAR9 =bt.If(VAR8!=0,(self.datas[0].close - VAR8) / VAR8 * 100,0)
        self.VARA = bt.indicators.MovingAverageSimple(VAR9, period=2);
        self.VARA_Cross = CrossDown(self.VARA, -10)
        self.VARC_Cross=CrossUp(self.VARA, 10)
    def next(self):
        if self.VARA_Cross[0]==1:
            self.varb_count = 0
        else:
            self.varb_count += 1
        self.lines.VARB[0] = self.varb_count

        if self.VARC_Cross[0] == 1:
            self.varc_count = 0
        else:
            self.varc_count += 1
        self.lines.VARC[0] = self.varc_count

def get_akshare_data_hk(code='000001'):
    # 将代码转换为akshare格式
    if '.' in code:
        code = code.split('.')[0]
    # 使用akshare获取股票数据
    stock_zh_a_hist_df = ak.stock_hk_hist(symbol=code, period="daily", start_date="20200101", end_date="20230615",adjust="")
    # 重命名列以匹配之前的格式
    stock_zh_a_hist_df = stock_zh_a_hist_df.rename(columns={
        '日期': 'datetime',
        '开盘': 'open',
        '最高': 'high',
        '最低': 'low',
        '收盘': 'close',
        '成交量': 'vol',
        '成交额': 'amount',
        '振幅': 'amplitude',
        '涨跌幅': 'pct_chg',
        '涨跌额': 'change',
        '换手率': 'hsl'
    })

    # 转换日期格式
    stock_zh_a_hist_df['datetime'] = pd.to_datetime(stock_zh_a_hist_df['datetime'])

    # 添加代码列
    stock_zh_a_hist_df['code_1'] = int(code)

    return stock_zh_a_hist_df




if __name__ == '__main__':
    cerebro = bt.Cerebro()
    code = '00399.HK'
    strats = cerebro.optstrategy(TestStrategy,code=code)
    # dataframe = get_hst_data(code)  # 获取数据
    # dataframe = get_tdx_data(code)  # 获取数据
    dataframe = get_akshare_data_hk(code)
    data = akshare_datasource(dataname=dataframe)
    # df = yf.download("AAPL", start="2020-01-01", end="2021-12-31")
    # data = hst_datasource(dataname=dataframe)
    # data = tdx_datasource(dataname=dataframe)
    cerebro.adddata(data)
    # cerebro.addindicator(大盘指数,code=code)
    cerebro.addindicator(黄金坑稳赚买_indicator, code=code)
    cerebro.broker.setcash(100000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.001)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)
