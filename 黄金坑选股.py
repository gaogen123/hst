import baostock as bs
import 函数库 as my_fun
from MyTT import *
from my_tool import *
from 筹码分布 import ChipDistribution
import 尊贵版2
import 资金斜率
import 吸筹斜率
import 黄金坑稳赚买

#获取btc.usdt交易对120日的数据
# df=get_price('btc.usdt',count=120,frequency='1d');     #'1d'是1天, '4h'是4小时
a = ChipDistribution()
code = 'sh.600084'
name=my_fun.query_stock_basic(code)['code_name'][0]
start_date='2023-05-25'
end_date='2024-05-31'
a.get_data(code, start_date, end_date)  # 获取数据
df=a.data


去ST=(IF(my_fun.NAMELIKE(name,'ST'),0,1)) & (IF(my_fun.NAMELIKE(name,'*ST'),0,1));
去科创板=IF(my_fun.CODELIKE(code,'688'),0,1);
去创业板=IF(my_fun.CODELIKE(code,'300'),0,1);
去北交所股票=(IF(my_fun.CODELIKE(code,'82'),0,1)) & (IF(my_fun.CODELIKE(code,'83'),0,1)) & (IF(my_fun.CODELIKE(code,'87'),0,1)) & (IF(my_fun.CODELIKE(code,'88'),0,1));
选股=(去ST==1) & (去科创板==1) & (去创业板==1) & (去北交所股票==1);
# 前面有一段下跌趋势
新一轮启动=(BARSLASTCOUNT(REF(资金斜率.斜率<0,1))>=3) & (BARSLASTCOUNT (REF(吸筹斜率.斜率>0,1))>=3);
# 当前周期资金斜率和筹码斜率良好
趋势良好=(资金斜率.斜率>0) & (吸筹斜率.斜率<0);
# 前面N个周期内出现稳赚买
前面出现稳赚买=EXIST(黄金坑稳赚买.稳赚买==30,5);
黄金坑=黄金坑稳赚买.黄金坑<0;
# 黄金坑趋势线开始往上走
黄金坑斜率=SLOPE(黄金坑稳赚买.黄金坑,2)>0
买入=选股 & 黄金坑 & 新一轮启动 & 趋势良好 & 前面出现稳赚买 & 黄金坑斜率;
# 包容算法
卖出=(吸筹斜率.斜率>1.5) | (资金斜率.斜率<-2);
# 多头买入(买开)
ENTERLONG:my_fun.TFILTER(买入,卖出,1);
# 多头卖出(卖平)
EXITLONG:my_fun.TFILTER(买入,卖出,2);
