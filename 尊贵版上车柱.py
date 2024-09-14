import baostock as bs
import 函数库 as my_fun
from MyTT import *
from my_tool import *
from 筹码分布 import ChipDistribution
import 尊贵版2
import 资金斜率
import 吸筹斜率
import 黄金坑稳赚买

code = 'sh.600084'
name=my_fun.query_stock_basic(code)['code_name'][0]

去ST=IF(my_fun.NAMELIKE(name,'ST'),0,1) & IF(my_fun.NAMELIKE(name,'*ST'),0,1);
去科创板=IF(my_fun.CODELIKE(code,'688'),0,1);
去创业板=IF(my_fun.CODELIKE(code,'300'),0,1);
去北交所股票=IF(my_fun.CODELIKE(code,'82'),0,1) & IF(my_fun.CODELIKE(code,'83'),0,1) & IF(my_fun.CODELIKE(code,'87'),0,1) & IF(my_fun.CODELIKE(code,'88'),0,1);
选股=(去ST==1) & (去科创板==1) & (去创业板==1) & (去北交所股票==1);
黄金坑买信号=REF(黄金坑稳赚买.黄金坑,1)<0;
# 当前周期资金斜率>2
资金斜率阈值=资金斜率.斜率>=2;
# 前一根资金斜率-当前资金斜率>=2
资金斜率下降=REF(资金斜率.斜率,1)-资金斜率.斜率>=2;
# 当前吸筹斜率-前一根吸筹斜率>0
吸筹斜率下降=ABS(REF(吸筹斜率.斜率,1))-ABS(吸筹斜率.斜率)>0;
卖出1= (吸筹斜率.斜率>0) | (资金斜率.斜率<0);
买入= 选股 & (尊贵版2.庄家线>尊贵版2.警戒线) & (尊贵版2.资金线<尊贵版2.黄线上买入) & (尊贵版2.上车柱==1) & (吸筹斜率.斜率<0) & (资金斜率.斜率>0)  & 黄金坑买信号 & 资金斜率阈值;
卖出=卖出1;
# 多头买入(买开)
ENTERLONG=my_fun.TFILTER(买入,卖出,1);
# 多头卖出(卖平)
EXITLONG=my_fun.TFILTER(买入,卖出,2);