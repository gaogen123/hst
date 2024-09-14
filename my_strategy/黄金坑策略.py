from concurrent.futures import ThreadPoolExecutor, as_completed
import backtrader as bt
import psycopg2
from psycopg2 import sql
from pytdx.hq import TdxHq_API

from cust_indicator.吸筹斜率 import 吸筹斜率
from cust_indicator.斜率_BarsLastCount import 斜率_BarsLastCount
from cust_indicator.资金斜率 import 资金斜率
from cust_indicator.黄金坑2日斜率 import 黄金坑2日斜率_indc
from cust_indicator.黄金坑稳赚买 import 黄金坑稳赚买_indicator
from datasource.akshare_datasource import akshare_datasource
from datasource.tdx_datasource import tdx_datasource
from my_tool import *
import akshare as ak


class TestStrategy(bt.Strategy):
    params = (
        ('period', 2),
        ('code', None),
        ('backtest_time', None),
    )

    def stop(self):
        self.roi = (self.broker.get_value() / self.broker.startingcash) - 1
        self.log(f'ROI: {self.roi:.2f}')

    def __init__(self):
        # 去ST:=IF(NAMELIKE('ST'),0,1) AND IF(NAMELIKE('*ST'),0,1);
        # 去科创板:=IF(CODELIKE('688'),0,1);
        # 去创业板:=IF(CODELIKE('300'),0,1);
        # 去北交所股票:=IF(CODELIKE('82'),0,1) AND IF(CODELIKE('83'),0,1) AND IF(CODELIKE('87'),0,1) AND IF(CODELIKE('88'),0,1);
        # 选股:=去ST AND 去科创板 AND 去创业板 AND 去北交所股票;
        self.资金斜率连续满足条件周期数 = 斜率_BarsLastCount(self.data, code=self.params.code).资金斜率_count
        self.吸筹斜率连续满足条件周期数 = 斜率_BarsLastCount(self.data, code=self.params.code).吸筹斜率_count
        self.新一轮启动 = bt.And(self.资金斜率连续满足条件周期数 >= 3, self.吸筹斜率连续满足条件周期数 >= 3)
        资金_斜率 = 资金斜率(self.data, code=self.params.code).资金斜率
        吸筹_斜率 = 吸筹斜率(self.data, code=self.params.code).吸筹斜率
        趋势良好 = bt.And(资金_斜率 > 0, 吸筹_斜率 < 0)
        self.前面出现稳赚买 = EXIST_黄金坑(self.data, period=5, code=self.params.code).exist
        黄金坑稳赚买 = 黄金坑稳赚买_indicator(self.data, code=self.params.code)
        self.黄金坑 = bt.And(黄金坑稳赚买.黄金坑_line < 0)
        黄金坑2日斜率 = 黄金坑2日斜率_indc(self.data, code=self.params.code).黄金坑斜率_line
        self.黄金坑斜率 = bt.And(黄金坑2日斜率 > 0)  # 黄金坑趋势线开始往上走
        self.买入 = bt.And(self.黄金坑 > 0, self.新一轮启动 > 0, 趋势良好 > 0, self.前面出现稳赚买 > 0,
                           self.黄金坑斜率 > 0)
        self.卖出 = bt.Or(吸筹_斜率 > 1.5, 资金_斜率 < -2)  # 包容算法
        # {多头买入(买开)} ENTERLONG:TFILTER(买入,卖出,1);
        # {多头卖出(卖平)}EXITLONG:TFILTER(买入,卖出,2);

    import psycopg2
    from psycopg2 import sql

    def write_backtest_log(self, code, strategy_name, type, price, trigger_time):
        try:
            # 连接到PostgreSQL数据库
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="123",
                host="localhost",
                port="5432"
            )
            
            # 创建游标对象
            cur = conn.cursor()
            
            # 准备SQL语句
            insert_query = sql.SQL("""
                INSERT INTO strategy_backtest (code, strategy_name, type, price, trigger_time,backtest_time)
                VALUES (%s, %s, %s, %s, %s, %s)
            """)
            
            # 执行SQL语句
            cur.execute(insert_query, (code, strategy_name, type, price, trigger_time, self.p.backtest_time,))
            
            # 提交事务
            conn.commit()
            
            self.log(f"回测日志已成功写入数据库: {code}, {strategy_name}, {type}, {price}, {trigger_time},{self.p.backtest_time}")
        
        except (Exception, psycopg2.Error) as error:
            self.log(f"写入数据库时发生错误: {error}")
        
        finally:
            # 关闭游标和连接
            if conn:
                cur.close()
                conn.close()

    def log(self, txt, dt=None):
        ''' 此策略的日志功能'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 向/由经纪人提交/接受买入/卖出订单
            return

        # 检查订单是否已完成
        # 注意：如果现金不足，券商可能会拒绝订单
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED for {self.data.code[0]}, %.2f' % order.executed.price)
                self.write_backtest_log(code=self.data.code[0], strategy_name='黄金坑策略', type='买入', price=order.executed.price, trigger_time=self.datas[0].datetime.date(0).isoformat())
            elif order.issell():
                self.log(f'SELL EXECUTED for {self.data.code[0]}, %.2f' % order.executed.price)
                self.write_backtest_log(code=self.data.code[0], strategy_name='黄金坑策略', type='卖出', price=order.executed.price, trigger_time=self.datas[0].datetime.date(0).isoformat())
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'Order Canceled/Margin/Rejected for {self.data.code[0]}')

        # 设置为没有待处理的订单
        self.order = None

    def next(self):
        if not self.position:
            if self.买入[0]:
                self.buy()
        else:
            if self.卖出[0]:
                self.sell()

        # print(f'''
        #         日期:{self.datas[0].datetime.date(0).isoformat()}
        #         资金斜率连续满足条件周期数:{self.资金斜率连续满足条件周期数[0]}
        #         吸筹斜率连续满足条件周期数:{self.吸筹斜率连续满足条件周期数[0]}
        #         新一轮启动:{self.新一轮启动[0]}
        #         前面出现稳赚买:{self.前面出现稳赚买[0]}
        #         黄金坑:{self.黄金坑[0]}
        #         黄金坑斜率:{self.黄金坑斜率[0]}
        #         买入:{self.买入[0]}
        #         卖出:{self.卖出[0]}
        # '''
        # )


class EXIST_黄金坑(bt.Indicator):
    lines = ('exist',)
    params = (
        ('period', 5),
        ('code', None)
    )

    def __init__(self):
        self.稳赚买_line = 黄金坑稳赚买_indicator(self.data, code=self.params.code).稳赚买_line

    def next(self):
        # print(f'''
        #                 日期:{self.datas[0].datetime.date(0).isoformat()}
        #                 稳赚买:{self.稳赚买_line[0]}
        #         '''
        #       )
        for i in range(self.p.period):
            if i + 1 > len(self):
                break
            if self.稳赚买_line[-i] == 30:
                self.lines.exist[0] = 5
                return
        self.lines.exist[0] = 0


def get_tdx_data(code='000001'):
    code_1 = code.split('.')[0]
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        data = api.to_df(api.get_security_bars(9, 1, code_1, 0, 500))  # 返回DataFrame
    tdx_liutongguben = get_tdx_liutongguben(code_1)
    data['hsl'] = data['vol'] / tdx_liutongguben
    data['datetime'] = pd.to_datetime(data['datetime'])
    data['code'] = int(code_1)
    return data



def get_tdx_liutongguben(code):
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        data = api.to_df(api.get_finance_info(1, code))  # 返回DataFrame
    return data['liutongguben'][0]


# 更新get_akshare_data函数以包含换手率计算
def get_akshare_data(code='000001'):
    # 将代码转换为akshare格式
    if '.' in code:
        code = code.split('.')[0]

    # 使用akshare获取股票数据
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date="20200101", end_date="20230615",
                                            adjust="qfq")

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
    stock_zh_a_hist_df['code'] = code

    return stock_zh_a_hist_df


def run_backtest(code,backtest_time):
    cerebro = bt.Cerebro()
    strats = cerebro.addstrategy(TestStrategy, code=code,backtest_time=backtest_time)

    dataframe = get_tdx_data(code)
    data = tdx_datasource(dataname=dataframe)
    cerebro.adddata(data)

    cerebro.broker.setcash(10000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=1000)
    cerebro.broker.setcommission(commission=0.001)

    # 添加分析器
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade')

    try:
        print(f'开始回测 {code}')
        print(f'初始投资组合价值 for{code}: %.2f' % cerebro.broker.getvalue())
        results = cerebro.run()
        strat = results[0]

        # 获取分析结果
        roi = strat.analyzers.returns.get_analysis()['rnorm100']
        trade_analyzer = strat.analyzers.trade.get_analysis()

        total_trades = trade_analyzer.total.total if 'total' in dir(trade_analyzer) else 0
        won_trades = trade_analyzer.won.total if 'won' in dir(trade_analyzer) else 0
        win_rate = (won_trades / total_trades * 100) if total_trades > 0 else 0

        print(f'最终投资组合价值 for{code}: %.2f' % cerebro.broker.getvalue())
        print(f'{code} 收益率: {roi:.2f}%')
        print(f'{code} 胜率: {win_rate:.2f}%')
        print('----------------------------')

        return code, {'roi': roi, 'win_rate': win_rate}
    except Exception as e:
        print(f"{code}:回测过程中发生错误: {e}")

if __name__ == '__main__':
    from datetime import datetime
    # 获取当前时间并格式化
    backtest_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stock_info_sh_name_code_df = ak.stock_info_sh_name_code(symbol="主板A股")
    stock_codes = stock_info_sh_name_code_df['证券代码'].tail(200).tolist()
    final_results = {}
    # run_backtest(code='600055.SH')
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(run_backtest, code,backtest_time): code for code in stock_codes}
        for future in as_completed(futures):
            try:
                code, result = future.result()
                final_results[code] = result
            except Exception as e:
                print(f"{code}:执行过程中发生错误: {e}")

    # 打印所有股票的回测结果
    print("\n所有股票的回测结果:")
    for code, result in final_results.items():
        print(f"{code}: 收益率 {result['roi']:.2f}%, 胜率 {result['win_rate']:.2f}%")

    # 计算平均收益率和平均胜率
    avg_roi = sum(result['roi'] for result in final_results.values()) / len(final_results) if len(final_results)>0 else 0
    avg_win_rate = sum(result['win_rate'] for result in final_results.values()) / len(final_results) if len(final_results)>0 else 0
    print(f"\n平均收益率: {avg_roi:.2f}%")
    print(f"平均胜率: {avg_win_rate:.2f}%")



