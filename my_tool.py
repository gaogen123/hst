import pandas as pd


def winner_core(ContextInfo, close):
    close_price = close[-1]

    # 获取上市日期
    # ipo_date = ContextInfo.get_open_date(ContextInfo.get_universe()[0])
    df = ContextInfo.get_market_data(['volume', 'amount'], stock_code=ContextInfo.get_universe(), skip_paused=True,
                                     period='1d', dividend_type='front', end_time=close.index[-1], count=250)
    df = df.loc[df['volume'] != 0]
    df['mean'] = df['amount'] / df['volume'] / 100
    turnover_rate = ContextInfo.get_turnover_rate(ContextInfo.get_universe(), df.index[0], df.index[-1])
    df['turnover'] = turnover_rate['000001.SZ'].values
    df['turnover'][0] = 0
    # 1减去换手率
    df['1_turnover'] = 1 - df['turnover']
    df['2_turnover'] = df['1_turnover'][::-1].values
    df['3_turnover'] = df['2_turnover'].shift(periods=1)
    df['3_turnover'][0] = 1
    # print(df[['1_turnover', '2_turnover', '3_turnover']])
    df['4_turnover'] = df['3_turnover'].cumprod()[::-1].values
    df['turnover'][0] = 1
    df['chouma'] = df['turnover'] * df['4_turnover']
    return df.loc[df['mean'] < close_price]['chouma'].sum()


def winner(ContextInfo, close):
    result = []
    n = len(close)
    for i in range(n):
        res = winner_core(ContextInfo, close[: i + 1])
        result.append(res)
    return pd.Series(result, index=close.index)