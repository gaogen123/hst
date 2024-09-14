from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json

import backtrader as bt
import baostock as bs
import requests
from backtrader.indicators import CrossOver
from pytdx.hq import TdxHq_API

from cust_indicator.BARSCOUNT import BARSCOUNT
from cust_indicator.COUNT_indicator import COUNT_indicator
from cust_indicator.CustomEMA import CustomEMA
from datasource.tdx_datasource import tdx_datasource
from my_tool import *


class 主力建仓尊贵版_indicator(bt.Indicator):
    lines = (
        '量能',
        '线',
        '资金线',
        '吸筹',
        '庄家线',
        '大资金',
        '上车柱',
    )
    params = (
        ('code',None),
    )

    def __init__(self):
        VALID = 1;
        M1 = 55;
        VAR1 = 1
        self.昨日最低价=self.datas[0].low(-1)
        self.今日最低价=self.datas[0].low
        self.VAR2A = self.datas[0].low(-1) * VAR1 * VALID;
        self.分子abs=abs(self.datas[0].low - self.VAR2A)
        self.分子 = CustomEMA(abs(self.datas[0].low - self.VAR2A), period=3,weight=1)
        self.分母 = CustomEMA(bt.indicators.Max(self.datas[0].low - self.VAR2A, 0), period=3 ,weight=1)
        self.分母=bt.If(self.分母==0,0.01,self.分母)
        self.VAR3A=bt.If(self.分母!=0,self.分子/self.分母*100,0)
        VAR4A = bt.indicators.EMA(bt.If(self.datas[0].close * 1.3, self.VAR3A * 10, self.VAR3A / 10), period=3) * VAR1 * VALID;
        VAR5A=bt.indicators.Lowest(self.datas[0].low, period=30) * VAR1 * VALID
        VAR6A = bt.indicators.Highest(VAR4A, period=30) * VAR1 * VALID;
        VAR7A = bt.If(bt.indicators.MovingAverageSimple(self.datas[0].close, period=58), 1, 0) * VAR1;
        VAR8A = bt.If(618 * VAR7A * VAR1 * VALID!=0,bt.indicators.EMA(bt.If(self.datas[0].low <= VAR5A, (VAR4A + VAR6A * 2) / 2, 0), period=3) / 618 * VAR7A * VAR1 * VALID,0)
        BBA = bt.If(VAR8A * VALID > 100, 100, VAR8A) * VAR1;
        N = 31;
        K1 = 3;
        self.lines.量能 =bt.If((bt.indicators.Highest(self.datas[0].high, period=N) - bt.indicators.Lowest(self.datas[0].low,
                                                                                          period=N)) != 0,bt.indicators.EMA(100 * (self.datas[0].close - bt.indicators.Lowest(self.datas[0].low, period=N)) / (bt.indicators.Highest(self.datas[0].high, period=N) - bt.indicators.Lowest(self.datas[0].low, period=N)),
                   period=K1) / 1 * VALID,0 )
        self.黄线上买入 = 38 * VALID
        self.警戒线 = 85 * VALID
        self.lines.吸筹 = bt.If(BBA * VALID > 0, BBA * VALID, 0)
        吸筹1 = bt.If(BBA * VALID > 0, BBA * VALID, 0)
        # STICKLINE(吸筹1>-100,0,吸筹1,3,0),,COLORBLUE;
        BA2 =bt.If(bt.indicators.Highest(self.datas[0].high, period=M1) - bt.indicators.Lowest(self.datas[0].low, period=M1)!=0,100 * (bt.indicators.Highest(self.datas[0].high, period=M1) - self.datas[0].close) / (bt.indicators.Highest(self.datas[0].high, period=M1) - bt.indicators.Lowest(self.datas[0].low, period=M1)),0)
        # 庄家建仓=IF(VAR8A>100,100,VAR8A),COLORBLUE;
        庄家建仓 = bt.If(VAR8A > 100, 100, VAR8A)
        # STICKLINE(庄家建仓>-100,0,庄家建仓,3,0)*VAR1,,COLORBLUE;
        # 线:IF(BA2*VALID>0,BA2*VALID,DRAWNULL),NODRAW;
        self.lines.线 = bt.If(BA2 * VALID > 0, BA2 * VALID, 0);
        RSV = bt.If(bt.indicators.Highest(self.datas[0].high, period=N) - bt.indicators.Lowest(self.datas[0].low, period=N)!=0,(self.datas[0].close - bt.indicators.Lowest(self.datas[0].low, period=N)) / (bt.indicators.Highest(self.datas[0].high, period=N) - bt.indicators.Lowest(self.datas[0].low, period=N)) * 100,0) ;
        K = CustomEMA(RSV, period=3,weight=1);
        D = CustomEMA(K, period=3,weight=1);
        J = 3 * K - 2 * D;
        self.lines.资金线 = bt.If(bt.indicators.EMA(J, period=6) * VALID, bt.indicators.EMA(J, period=6),0)
        self.VARC5 = bt.indicators.Lowest(self.datas[0].low, period=75) * VALID;
        self.VARC6 = bt.indicators.Highest(self.datas[0].high, period=75) * VALID;
        self.VARC7 = (self.VARC6 - self.VARC5) / 100 * VALID;
        self.VARC8 = bt.If(self.VARC7!=0,CustomEMA((self.datas[0].close - self.VARC5) / self.VARC7,period=20,weight=1),0);
        self.VARCA = 3 * self.VARC8 - 2 * CustomEMA(self.VARC8,period=15,weight=1);
        self.lines.庄家线 = bt.If((100 - self.VARCA) * VALID, (100 - self.VARCA) * VALID, 0)
        X = self.资金线 * VALID;
        Y = self.线 * VALID;
        self.VAR17=BARSCOUNT(condition=self.datas[0].close != None)-1
        VARF = bt.If(
                        bt.And(
                                    (bt.indicators.Highest(self.datas[0].high, period=75) - bt.indicators.Lowest(self.datas[0].low, period=75))!=0
                                    ,bt.indicators.Highest(self.datas[0].high, period=75) - bt.indicators.Lowest(self.datas[0].low, period=75)!=0
                              )
                        ,100 - 3 * CustomEMA((self.datas[0].close - bt.indicators.Lowest(self.datas[0].low, period=75)) / (bt.indicators.Highest(self.datas[0].high, period=75) - bt.indicators.Lowest(self.datas[0].low, period=75)) * 100, period=20,weight=1) + 2 * CustomEMA(CustomEMA((self.datas[0].close - bt.indicators.Lowest(self.datas[0].low, period=75)) / (bt.indicators.Highest(self.datas[0].high, period=75) - bt.indicators.Lowest(self.datas[0].low, period=75)) * 100, period=20,weight=1), period=15,weight=1) * VALID
                        ,0
                    )

        VAR10=bt.If(
            bt.And(
                bt.indicators.Highest(self.datas[0].high, period=75) - bt.indicators.Lowest(self.datas[0].low,period=75) != 0
                , bt.indicators.Highest(self.datas[0].high, period=75) - bt.indicators.Lowest(self.datas[0].low,period=75) != 0
            )
            ,100 - 3 * CustomEMA((self.datas[0].open - bt.indicators.Lowest(self.datas[0].low, period=75)) / (bt.indicators.Highest(self.datas[0].high, period=75) - bt.indicators.Lowest(self.datas[0].low, period=75)) * 100, period=20,weight=1) + 2 * CustomEMA(CustomEMA((self.datas[0].open - bt.indicators.Lowest(self.datas[0].low, period=75)) / (bt.indicators.Highest(self.datas[0].high, period=75) - bt.indicators.Lowest(self.datas[0].low, period=75)) * 100, period=20), period=15) * VALID
            ,0
        )

        VAR11 = bt.And(VARF < VAR10(-1),self.datas[0].volume > self.datas[0].volume(-1),self.datas[0].close > self.datas[0].close(-1) * VALID)
        self.lines.大资金 = bt.And(VAR11 * VALID,COUNT_indicator(condition=VAR11, period=30)==1)
        # # DRAWTEXT(VAR11*VALID AND COUNT(VAR11,30)=cust_indicator*VALID,97*VALID,'大资金'),LINETHICK1,COLORFF00FF;
        # # STICKLINE(VAR11*VALID AND COUNT(VAR11,30)=cust_indicator,cust_indicator,85,2,0)*VALID,COLORFF00FF,LINETHICK4;
        VAR200 = bt.If(
                            bt.indicators.Highest(self.datas[0].high, period=20) - bt.indicators.Lowest(self.datas[0].low, period=20)!=0
                            ,(self.datas[0].close - bt.indicators.Lowest(self.datas[0].low, period=20)) / (bt.indicators.Highest(self.datas[0].high, period=20) - bt.indicators.Lowest(self.datas[0].low, period=20)) * 100 * VALID
                            ,0
                      )
        VAR300 = CustomEMA(CustomEMA(VAR200, period=3), period=3) / 28.57;
        VAR400 = bt.indicators.EMA(VAR300, period=5) * VALID;
        操盘 = 3 * VAR300 - 2 * VAR400 * VALID;
        self.lines.上车柱 = bt.And(CrossOver(操盘, VAR300) * VALID>0 , VAR300 < 2.1 , self.datas[0].close > self.datas[0].open)
        # 上车柱_1 = CrossOver(操盘, VAR300) * VALID
        # 上车柱_2 = VAR300 < 2.1
        # 上车柱_3 = self.datas[0].close > self.datas[0].open

    # def next(self):
    #     print(f'''
    #     日期:{self.datas[0].datetime.date(0).isoformat()}
    #                        VAR2A:{self.VAR2A[0]}
    #                        昨日最低价:{self.昨日最低价[0]}
    #                        今日最低价:{self.今日最低价[0]}
    #                        分子abs:{self.分子abs[0]}
    #                        分子:{self.分子[0]}
    #                        分母:{self.分母[0]}
    #                        VAR3A:{self.VAR3A[0]}
    #                        量能:{self.量能[0]}
    #                        线:{self.线[0]}
    #                        资金线:{self.资金线[0]}
    #                        庄家线:{self.庄家线[0]}
    #                        大资金:{self.大资金[0]}
    #                        上车柱:{self.上车柱[0]}
    #
    #                   ''')

    # 获取流通股本
    def get_net_profit(year, quarter):
        # 登陆系统
        lg = bs.login()

        # 显示错误信息
        print('login respond error_code:' + lg.error_code)
        print('login respond  error_msg:' + lg.error_msg)
        # 获取股票流通股本信息
        rs_profit = bs.query_profit_data(code, year=year, quarter=quarter)
        print('query_profit_data respond error_code:' + rs_profit.error_code)
        print('query_profit_data respond  error_msg:' + rs_profit.error_msg)

        # 打印结果
        profit_list = []
        while (rs_profit.error_code == '0') & rs_profit.next():
            profit_list.append(rs_profit.get_row_data())

        result = pd.DataFrame(profit_list, columns=rs_profit.fields)

        # 获取流通股本字段
        float_share = result.loc[0, "liqaShare"]
        return float_share


class TestStrategy(bt.Strategy):
    params = (
        ('code', None),
    )

    def __init__(self):
        # code = self.params.code
        # self.主力建仓尊贵版_indicator = 主力建仓尊贵版_indicator(self.data,code=code)
        pass


def get_hst_data(code, start_date='2024-01-01'):
    url = 'http://127.0.0.1:11111/hq/KL'
    kw = {
        "timeout_sec": 10,
        "params": {
            "security": {
                "dataType": "30000",
                "code": code
            },
            # "startDate": "20240101",
            "startDate": start_date.replace('-',''),
            "direction": "1",
            "exRightFlag": "0",
            "cycType": "2",
            "limit": "600"
        }
    }
    json_str = json.dumps(kw)
    response = requests.post(url, data=json_str)
    pd_data = pd.read_json(json.dumps(json.loads(response.text)['data']['kline']))

    pd_data = pd_data.set_index('date', drop=False)
    # pd_data=pd_data.set_index('date',drop=False).rename(columns={'closePrice': 'close', 'highPrice': 'high', 'openPrice': 'open', 'volume': 'volume','lowPrice':'low'})
    return pd_data


def get_tdx_data(code='000001'):
    code=code.split('.')[0]
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        data = api.to_df(api.get_security_bars(9, 1, code, 0, 500))  # 返回DataFrame
    tdx_liutongguben = get_tdx_liutongguben(code)
    data['hsl']=data['vol']/tdx_liutongguben if tdx_liutongguben!=0 else 0
    data['datetime'] = pd.to_datetime(data['datetime'])
    return data


def get_tdx_liutongguben(code):
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        data = api.to_df(api.get_finance_info(1, code))  # 返回DataFrame
    return data['liutongguben'][0]



if __name__ == '__main__':
    cerebro = bt.Cerebro()
    code = '601398.SH'
    strats = cerebro.optstrategy(
        TestStrategy,code=code)
    # dataframe = get_hst_data(code)  # 获取数据
    dataframe = get_tdx_data(code)  # 获取数据
    # df = yf.download("AAPL", start="2020-01-01", end="2021-12-31")
    # data = hst_datasource(dataname=dataframe)
    data = tdx_datasource(dataname=dataframe)
    cerebro.adddata(data)
    cerebro.addindicator(主力建仓尊贵版_indicator, code=code)
    cerebro.broker.setcash(100000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.001)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)
