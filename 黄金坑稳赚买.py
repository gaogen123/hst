from  hb_hq_api import *
from  MyTT import *
from my_tool import *
from 筹码分布 import ChipDistribution
import seaborn as sns
import matplotlib.pyplot as plt
import baostock as bs
import 函数库 as my_fun

#获取btc.usdt交易对120日的数据
# df=get_price('btc.usdt',count=120,frequency='1d');     #'1d'是1天, '4h'是4小时
a = ChipDistribution()
code = 'sh.600084'
start_date='2022-07-19'
end_date='2024-05-31'
a.get_data(code,start_date, end_date)  #获取数据
a.calcuChip(flag=1, AC=1) #计算
a.get_data(code, start_date, end_date)  # 获取数据
df=a.data
#流通股本
CAPITAL= float(my_fun.get_net_profit(code,year=2024, quarter=1))
INDEXC=my_fun.get_large_cap(code,start_date,end_date)['close'].values.astype(float)
INDEXL=my_fun.get_large_cap(code,start_date,end_date)['low'].values.astype(float)
INDEXH=my_fun.get_large_cap(code,start_date,end_date)['high'].values.astype(float)


VAR1=MA(a.winner(),9)*100;
买= CROSS(VAR1,2)*30
VAR2=(1-EMA((HHV(df.high.values,15)-df.close.values)/(HHV(df.high.values,15)-LLV(df.low.values,15)),15))*100;
VAR3=(df.close.values-LLV(df.low.values,21))/(HHV(df.high.values,21)-LLV(df.low.values,21))*100;
VAR4=SMA(VAR3,9,1);
VAR5=SMA(VAR4,9,1);
VAR6=(df.close.values-SMA(df.close.values,13,1))/SMA(df.close.values,13,1)*(-100);
VAR7=(REF(VAR6,1)>13) & (REF(VAR6,1)/VAR6>1.23) & (df.close.values/REF(df.close.values,1)>1.03);
春笋 = IF((VAR7) & (REF(df.close.values, 1) <= np.asarray(a.cost(5))), 20, 0)
VAR8=MA(df.close.values,27);
VAR9=(df.close.values-VAR8)/VAR8*100;
VARA=MA(VAR9,2);
VARB=my_fun.BARSLAST(CROSS(-10,VARA)==1)
VARC=my_fun.BARSLAST(CROSS(VARA,10)==1)
VARD=(VARA<-10) & (VARB>3);
VARE=(VARA>10) & (VARC>3);
黄金坑= IF(VARD,VARA,0);
财神到= IF(VARE,VARA,0)
稳赚买= IF((VARA>REF(VARA,1)) & (VARD) & (VARA<-15),30,0)
# DRAWICON(稳赚买>0,40,cust_indicator);
VARF=REF(df.low.values,1)*0.9;
VAR10=df.low.values*0.9;
VAR11=(VAR10*df.volume+VARF*(CAPITAL-df.volume))/CAPITAL;
VAR12=EMA(VAR11,30);
VAR13=df.close.values-REF(df.close.values,1);
VAR14=MAX(VAR13,0);
VAR15=ABS(VAR13);
VAR16=SMA(VAR14,7,1)/SMA(VAR15,7,1)*100;
VAR17=SMA(VAR14,13,1)/SMA(VAR15,13,1)*100;
VAR18=my_fun.BARSCOUNT(df.close.values);
VAR19=SMA(MAX(VAR13,0),6,1)/SMA(ABS(VAR13),6,1)*100;
VAR1A=(-200)*(HHV(df.high.values,60)-df.close.values)/(HHV(df.high.values,60)-LLV(df.low.values,60))+100;
VAR1B=(df.close.values-LLV(df.low.values,15))/(HHV(df.high.values,15)-LLV(df.low.values,15))*100;
VAR1C=SMA((SMA(VAR1B,4,1)-50)*2,3,1);
VAR1D=(INDEXC-LLV(INDEXL,14))/(HHV(INDEXH,14)-LLV(INDEXL,14))*100;
VAR1E=SMA(VAR1D,4,1);
VAR1F=SMA(VAR1E,3,1);
VAR20=(HHV(df.high.values,30)-df.close.values)/df.close.values*100;
VAR21=(VAR19<=25) & (VAR1A<-95) & (VAR20>20) & (VAR1C<-30) & (VAR1F<30) & (VAR12-df.close.values>=-0.25) & (VAR16<22) & (VAR17<28) & (VAR18>50);
超跌= VAR21