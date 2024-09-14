import backtrader as bt
import tushare as ts
import pandas as pd
from datetime import datetime
from pytdx.hq import TdxHq_API

from datasource.tdx_datasource import tdx_datasource
from my_strategy import 上车柱策略

# 设置 tushare 的 token
ts.set_token('c6c96e3dcc30fb44b35546bde250c118d08a1249d178106878e59125')
pro = ts.pro_api()


# 获取上证股票列表
def get_sse_stocks():
    data = pro.stock_basic(exchange='SSE', list_status='L')
    return data['ts_code'].tolist()


# 获取股票数据
def get_stock_data(code, start_date, end_date):
    df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
    df = df.sort_values('trade_date')
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df.set_index('trade_date', inplace=True)
    df['openinterest'] = 0
    df = df.rename(columns={'vol': 'volume'})
    return df

def get_tdx_data(code):
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        data = api.to_df(api.get_security_bars(9, 1, code, 0, 500))  # 返回DataFrame
    tdx_liutongguben = 1000
    data['hsl']=data['vol']/tdx_liutongguben
    data['datetime'] = pd.to_datetime(data['datetime'])
    data['code'] = code
    return data
def get_tdx_liutongguben(code):
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        data = api.to_df(api.get_finance_info(0, code))  # 返回DataFrame
    return data['liutongguben'][0]

# 主函数
def run_backtest(stock_code, start_date, end_date):
    cerebro = bt.Cerebro()

    # 获取数据
    # data = get_stock_data(stock_code, start_date, end_date)
    dataframe = get_tdx_data(stock_code)  # 获取数据
    data = tdx_datasource(dataname=dataframe)
    feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(feed)

    # 设置初始资金
    cerebro.broker.setcash(100000.0)

    # 添加策略
    cerebro.addstrategy(上车柱策略.TestStrategy)

    # 运行回测
    initial_value = cerebro.broker.getvalue()
    results = cerebro.run()
    final_value = cerebro.broker.getvalue()

    return (stock_code, initial_value, final_value)

def get_code_list():
    # 初始化API
    api = TdxHq_API()
    # 尝试连接到一个可用的服务器
    with api.connect('119.147.212.81', 7709):
        # 获取上证A股列表
        data = api.to_df(api.get_security_list(0, 0))
        # 获取前3个股票代码
        top_3_stocks = data['code'].head(3)
        return top_3_stocks
# 主程序
if __name__ == '__main__':
    start_date = '20200101'
    end_date = '20211231'

    # 获取上证股票列表
    sse_stocks = get_sse_stocks()

    # 运行回测
    results = []
    for stock in sse_stocks:
        try:
            result = run_backtest(stock, start_date, end_date)
            results.append(result)
            print(f"Completed backtest for {stock}")
        except Exception as e:
            print(f"Error in backtest for {stock}: {e}")

    # 输出结果
    results_df = pd.DataFrame(results, columns=['Stock', 'Initial Value', 'Final Value'])
    results_df['Return'] = (results_df['Final Value'] - results_df['Initial Value']) / results_df['Initial Value']
    results_df = results_df.sort_values('Return', ascending=False)
    print(results_df)

    # 保存结果
    results_df.to_csv('backtest_results.csv', index=False)
