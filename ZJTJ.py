#数字货币行情获取和指标计算演示
from  hb_hq_api import *
from  MyTT import *
from my_tool import *
from 筹码分布 import ChipDistribution
import seaborn as sns
import matplotlib.pyplot as plt

#获取btc.usdt交易对120日的数据
# df=get_price('btc.usdt',count=120,frequency='1d');     #'1d'是1天, '4h'是4小时
a = ChipDistribution()
code = 'sh.600571'
a.get_data(code,'2024-01-01', '2024-07-14')  # 获取数据
df=a.data

VAR1=EMA(EMA(df.close.values,9),9)
控盘=(VAR1-REF(VAR1,1))/REF(VAR1,1)*1000
# STICKLINE(控盘<0,控盘,0,cust_indicator,0),COLORWHITE;
A10=CROSS(控盘,0)
无庄控盘=IF(控盘<0,控盘,0)
开始控盘=IF(A10,5,0)
# STICKLINE(控盘>REF(控盘,cust_indicator) AND 控盘>0,控盘,0,cust_indicator,0),COLORRED;
有庄控盘=IF((控盘>REF(控盘,1)) & (控盘>0),控盘,0)
# VAR2:=100*WINNER(CLOSE*0.95);
a.calcuChip(flag=1, AC=1)  # 计算
成本分布=np.asarray(a.cost(85))   # 成本分布
VAR2=np.asarray(a.winner())*100

close=df.close.values
# STICKLINE(VAR2>50 AND COST(85)<CLOSE AND 控盘>0,控盘,0,cust_indicator,0),COLORFF00FF;
# 高度控盘:IF(VAR2>50 AND COST(85)<CLOSE AND 控盘>0,控盘,0),COLORFF00FF,NODRAW;
高度控盘=IF((VAR2>50) & (成本分布<df.close.values) & (控盘>0),控盘,0)
# STICKLINE(控盘<REF(控盘,cust_indicator) AND 控盘>0,控盘,0,cust_indicator,0),COLOR00FF00;
主力出货=IF((控盘<REF(控盘,1)) & (控盘>0),控盘,0)
# print(主力出货)
# 设置主题和颜色调色板
sns.set_theme(style="darkgrid", palette="pastel")
# 创建柱状图
sns.barplot(x=df['date'], y=开始控盘,)
# 显示图表
plt.show()

#入股无庄控盘不等于0显示无庄控盘值,否则比较开始控盘值,有庄控盘值,高度控盘值,主力出货值
# if 无庄控盘[0]!=0:
#     print('无庄控盘:',无庄控盘[0])
# else:
#

