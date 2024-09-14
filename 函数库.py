import numpy as np
import baostock as bs
import pandas as pd
# 之子转向同通达信zig函数
def zig(test,n):
    ZIG_STATE_START = 0
    ZIG_STATE_RISE = 1
    ZIG_STATE_FALL = 2
    x = n/100
    k = test
    peer_i = 0
    candidate_i = None
    scan_i = 0
    peers = [0]
    z = np.zeros(len(k))
    state = ZIG_STATE_START
    while True:
        scan_i += 1
        if scan_i == len(k) - 1:
            if candidate_i is None:
                peer_i = scan_i
                peers.append(peer_i)

            else:
                if state == ZIG_STATE_RISE:
                    if k[scan_i] >= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
                elif state == ZIG_STATE_FALL:
                    if k[scan_i] <= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
            break

        if state == ZIG_STATE_START:
            if k[scan_i] >= k[peer_i] * (1 + x):
                candidate_i = scan_i
                state = ZIG_STATE_RISE
            elif k[scan_i] <= k[peer_i] * (1 - x):
                candidate_i = scan_i
                state = ZIG_STATE_FALL
        elif state == ZIG_STATE_RISE:
            if k[scan_i] >= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] <= k[candidate_i] * (1 - x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_FALL
                candidate_i = scan_i
        elif state == ZIG_STATE_FALL:
            if k[scan_i] <= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] >= k[candidate_i] * (1 + x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_RISE
                candidate_i = scan_i
    for i in range(len(peers) - 1):
        peer_start_i = peers[i]
        peer_end_i = peers[i + 1]
        start_value = k[peer_start_i]
        end_value = k[peer_end_i]
        a = (end_value - start_value) / (peer_end_i - peer_start_i)
        for j in range(peer_end_i - peer_start_i + 1):
            z[j + peer_start_i] = start_value + a * j
    z=np.array(z)
    return z


#获取流通股本
def get_net_profit(code,year, quarter):
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

#获取上证指数,深证成指,创业板指,恒生指数的最高价
def get_large_cap(code,start_date,end_date):
    code1=code.split('.')[1]
    #上证
    if code1.startswith('600') or code1.startswith('601') or code1.startswith('603')or code1.startswith('605'):
        index_code='sh.000001'
    #深证
    if code1.startswith('000') or code1.startswith('200'):
        index_code='sz.399001'
    # 创业板
    if code1.startswith('300'):
        index_code='sz.399006'

    index_data_list = []
    bs.login()
    index_data = bs.query_history_k_data_plus(index_code, "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST", start_date=start_date,
                                                 end_date=end_date, frequency="d", adjustflag="3")
    while (index_data.error_code == '0') & index_data.next():
        index_data_list.append(index_data.get_row_data())
    index_data = pd.DataFrame(index_data_list, columns=index_data.fields)
    return index_data

# 上一次条件成立到当前的周期数
def BARSLAST(condition):

    # 初始化结果数组
    result = np.zeros_like(condition, dtype=int)

    # 记录上一个True元素的索引
    prev_true_idx = -1

    for i in range(len(condition)):
        if condition[i]:
            # 如果当前元素为True,更新上一个True元素的索引
            prev_true_idx = i
            result[i] = 0
        else:
            if prev_true_idx!=-1:
                result[i] = i - prev_true_idx
    return result

def BARSCOUNT(condition):
    """
    计算第一次条件成立到当前的周期数
    :param condition:
    :return:
    """
    # 初始化结果数组
    result = np.zeros_like(condition, dtype=int)

    # 记录上一个True元素的索引
    prev_true_idx = -1

    for i in range(len(condition)):
        if condition[i] and prev_true_idx == -1:
            # 如果当前元素为True,更新上一个True元素的索引
            prev_true_idx = i
            result[i] = 0
        else:
            if prev_true_idx != -1:
                result[i] = i - prev_true_idx
    return result
    # """
    # 计算第一次条件成立到当前的周期数
    # :param condition:
    # :return:
    # """
    # # 初始化结果数组
    # result = np.zeros_like(condition, dtype=int)
    #
    # # 记录上一个True元素的索引
    # prev_true_idx = np.where(condition, np.arange(len(condition)), -cust_indicator)
    # prev_true_idx = np.maximum.accumulate(prev_true_idx, axis=0)
    # result = np.arange(len(condition)) - prev_true_idx
    #
    # return result


def CODELIKE(code,startswith):
    # 使用NumPy的向量化操作判断每个元素是否以'a'开头
    np_code=np.array(pd.Series(code), dtype=str)
    return np.char.startswith(np_code, startswith)

def NAMELIKE(name,startswith):
    np_name=np.array(pd.Series(name), dtype=str)
    return np.char.startswith(np_name, startswith)

def query_stock_basic(code):
    # 登陆系统
    lg = bs.login()


    # 获取证券基本资料
    rs = bs.query_stock_basic(code)
    # rs = bs.query_stock_basic(code_name="浦发银行")  # 支持模糊查询

    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    # 登出系统
    bs.logout()
    return result

def TFILTER(condition_buy,condition_sell,sign):

    """
    过滤连续出现的信号
    :param condition_buy: 买入条件
    :param condition_sell: 卖出条件
    :param signal: 买入或卖出信号 cust_indicator:对买入信号过滤 2:对卖出信号过滤 0:对买入和卖出信号都过滤
    :return:买入信号或卖出信号
    """
    buy_result = np.zeros_like(condition_buy, dtype=bool)
    sell_result = np.zeros_like(condition_sell, dtype=bool)

    if sign==1:
        enterlong_last_buy_sign = False
        enterlong_last_sell_sign = False
        for i in range(len(condition_buy)):
            if condition_sell[i]:
                enterlong_last_buy_sign = False
                enterlong_last_sell_sign = True
            if condition_buy[i] and not enterlong_last_buy_sign and enterlong_last_sell_sign:
                buy_result[i] = True
                enterlong_last_buy_sign = True
                enterlong_last_sell_sign = False
        return buy_result
    elif sign==2:
        exitlong_last_buy_sign=False
        exitlong_last_sell_sign=False
        for i in range(len(condition_sell)):
            if condition_buy[i]:
                exitlong_last_sell_sign = False
                exitlong_last_buy_sign = True
            if condition_sell[i]  and not exitlong_last_sell_sign and exitlong_last_buy_sign:
                sell_result[i]=True
                exitlong_last_sell_sign=True
                exitlong_last_buy_sign = False
        return sell_result

def get_net_profit(code,year, quarter):
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
