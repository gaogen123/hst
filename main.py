# 这是一个示例 Python 脚本.sql。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

import akshare as ak
import talib
#数字货币行情获取和指标计算演示
from  hb_hq_api import *         #数字货币行情库
from  MyTT import *              #myTT麦语言工具函数指标库
import tushare as ts

import baostock as bs
import pandas as pd

import json

import yfinance as yf

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


def test1():
    code = "sz002241"
    df = ak.stock_zh_a_daily(symbol=code, start_date="20201203", end_date="20210115",
                             adjust="qfq")
    print(df.head())

def test2():
    # list of functions
    for name in talib.get_functions():
        print(name)

    # dict of functions by group
    for group, names in talib.get_function_groups().items():
        print(group)
        for name in names:
            print(f"  {name}")


def test3():
    # 获取btc.usdt交易对120日的数据
    df = get_price('btc.usdt', count=120, frequency='1d');  # '1d'是1天, '4h'是4小时


def test4():
    token = 'c6c96e3dcc30fb44b35546bde250c118d08a1249d178106878e59125'
    ts.set_token(token)
    pro = ts.pro_api()
    df = ts.pro_bar(ts_code='000001.SZ', start_date='20180101', end_date='20181011', factors=['tor', 'vr'])
    print(df)

from futu import *


def test5():
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    rs = bs.query_history_k_data_plus("sh.600000",
                                      "date,time,code,open,high,low,close,volume,amount,adjustflag",
                                      start_date='2017-07-01', end_date='2017-07-31',
                                      frequency="5", adjustflag="3")
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)


if __name__ == '__main__':
    # 创建 Ticker 对象，表示对 Microsoft 公司的股票数据进行操作
    msft = yf.Ticker('600519.SS')

    # 获取所有的股票信息
    # msft.info

    # 获取历史市场数据，这里是过去一个月的数据
    # hist = msft.history(period="1mo")

    # 显示历史数据的元信息（需要先调用 history() 函数）
    # msft.history_metadata

    # 显示公司行为信息（股利、拆股、资本收益）
    # msft.actions
    # msft.dividends
    # msft.splits
    # msft.capital_gains  # 仅适用于共同基金和交易所交易基金（etfs）


    # 显示股票股数
    data=msft.get_shares_full(start="2022-01-01", end=None)
    data = pd.DataFrame({'name': data})
    print(data.index)

    # 显示财务报表：
    # - 收入表
    msft.income_stmt
    msft.quarterly_income_stmt
    # - 资产负债表
    msft.balance_sheet
    msft.quarterly_balance_sheet
    # - 现金流量表
    msft.cashflow
    msft.quarterly_cashflow
    # 若要查看更多选项，请参考 `Ticker.get_income_stmt()`

    # 显示股东信息
    msft.major_holders
    msft.institutional_holders
    msft.mutualfund_holders

    # 显示未来和历史的盈利日期，返回最多未来4个季度和过去8个季度的数据，默认情况下。
    # 注意：如果需要更多信息，可以使用 msft.get_earnings_dates(limit=XX)，其中 XX 为增加的限制参数。
    msft.earnings_dates

    # 显示国际证券识别码（ISIN） - *实验性功能*
    # ISIN = International Securities Identification Number
    msft.isin

    # 显示期权到期日期
    msft.options

    # 显示新闻
    msft.news

    # 获取特定到期日的期权链
    opt = msft.option_chain('YYYY-MM-DD')
    # 数据可通过 opt.calls, opt.puts 获取



