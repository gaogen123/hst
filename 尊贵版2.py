import baostock as bs
import 函数库 as my_fun
from MyTT import *
from my_tool import *
from 筹码分布 import ChipDistribution

#获取btc.usdt交易对120日的数据
# df=get_price('btc.usdt',count=120,frequency='1d');     #'1d'是1天, '4h'是4小时
a = ChipDistribution()
code = 'sh.600084'
start_date='2023-05-25'
end_date='2024-05-31'
a.get_data(code, start_date, end_date)  # 获取数据
df=a.data


#获取流通股本

#流通股本
CAPITAL= float(my_fun.get_net_profit(code=code,year=2024, quarter=1))






INDEXC=my_fun.get_large_cap(code,start_date,end_date)['close'].values.astype(float)
INDEXL=my_fun.get_large_cap(code,start_date,end_date)['low'].values.astype(float)
INDEXH=my_fun.get_large_cap(code,start_date,end_date)['high'].values.astype(float)



VALID=1;
M1=55;
LC=REF(df.close.values,1);
RSI=((SMA(MAX((df.close.values - LC),0),3,1) / SMA(ABS((df.close.values - LC)),3,1)) * 100);
FF=EMA(df.close.values,3);
MA15=EMA(df.close.values,21);
VAR1=1
VAR2A=REF(df.low.values,1)*VAR1*VALID;
VAR3A=SMA(ABS(df.low.values-VAR2A),3,1)/SMA(MAX(df.low.values-VAR2A,0),3,1)*100*VAR1*VALID;
VAR4A=EMA(IF(df.close.values*1.3,VAR3A*10,VAR3A/10),3)*VAR1*VALID;
VAR5A=LLV(df.low.values,30)*VAR1*VALID;
VAR6A=HHV(VAR4A,30)*VAR1*VALID;
VAR7A=IF(MA(df.close.values,58),1,0)*VAR1;
VAR8A=EMA(IF(df.low.values<=VAR5A,(VAR4A+VAR6A*2)/2,0),3)/618*VAR7A*VAR1*VALID;
BBA=IF(VAR8A*VALID>100,100,VAR8A)*VAR1;
N=31;K1=3;
量能 =EMA(100*(df.close.values-LLV(df.low.values,N))/(HHV(df.high.values,N)-LLV(df.low.values,N)),K1)/1*VALID;
# DRAWICON(量能<cust_indicator*VALID,3,94);
黄线上买入 =38*VALID
警戒线 =85*VALID
# 吸筹=IF(BBA*VALID>0,BBA*VALID,DRAWNULL),COLORBLUE,NODRAW;
吸筹=IF(BBA*VALID>0,BBA*VALID,0)
吸筹1=IF(BBA*VALID>0,BBA*VALID,0)
# STICKLINE(吸筹1>-100,0,吸筹1,3,0),,COLORBLUE;
BA2= 100*(HHV(df.high.values,M1)-df.close.values)/(HHV(df.high.values,M1)-LLV(df.low.values,M1));
# 庄家建仓=IF(VAR8A>100,100,VAR8A),COLORBLUE;
庄家建仓=IF(VAR8A>100,100,VAR8A)
# STICKLINE(庄家建仓>-100,0,庄家建仓,3,0)*VAR1,,COLORBLUE;
# 线:IF(BA2*VALID>0,BA2*VALID,DRAWNULL),NODRAW;
线=IF(BA2*VALID>0,BA2*VALID,0);
RSV=(df.close.values-LLV(df.low.values,N))/(HHV(df.high.values,N)-LLV(df.low.values,N))*100;
K=SMA(RSV,3,1);
D=SMA(K,3,1);
J=3*K-2*D;
资金线=IF(EMA(J,6)*VALID,EMA(J,6),0)
资金线1=EMA(J,6)
VARC3=MA(df.close.values,13)*VALID;
VARC4=100-ABS((df.close.values-VARC3)/VARC3*100)*VALID;
VARC5=LLV(df.low.values,75)*VALID;
VARC6=HHV(df.high.values,75)*VALID;
VARC7=(VARC6-VARC5)/100*VALID;
VARC8=SMA((df.close.values-VARC5)/VARC7,20,1);
VARC9=SMA((df.open.values-VARC5)/VARC7,20,1);
VARCA=3*VARC8-2*SMA(VARC8,15,1);
VARCB=3*VARC9-2*SMA(VARC9,15,1);
VARCC=(100-VARCB);
庄家线=IF((100-VARCA)*VALID,(100-VARCA)*VALID,0)
X=资金线*VALID;
Y=线*VALID;
XG1=CROSS(X,Y)*VALID
# DRAWTEXT(XG1=cust_indicator,97,'金叉')*VALID,COLORYELdf.low.values;
VAR2=1/np.array(a.winner())*VALID;
# VAR2=cust_indicator/WINNER(df.close.values)*VALID;
VAR3=MA(df.close.values,13)*VALID;
VAR4=100-ABS((df.close.values-VAR3)/VAR3*100)*VALID;
VAR5=LLV(df.low.values,120)*VALID;
VAR6=HHV(df.high.values,120)*VALID;
VAR7=(VAR6-VAR5)/100*VALID;
VAR8=SMA((df.close.values-VAR5)/VAR7,20,1)*VALID;
VAR9=SMA((df.open.values-VAR5)/VAR7,20,1);
VARA=3*VAR8-2*SMA(VAR8,10,1);
VARB=3*VAR9-2*SMA(VAR9,10,1);
VARC=100-VARB;
VAREA=REF(df.low.values,1)*0.9*VALID;
VARFA=df.low.values*0.9*VALID;
VAR10A=(VARFA*df.volume.values+VAREA*(CAPITAL-df.volume.values))/CAPITAL;
VAR11A=EMA(VAR10A,30);
VAR12=df.close.values-REF(df.close.values,1);
VAR13=MAX(VAR12,0);
VAR14=ABS(VAR12)*VALID;
VAR15=SMA(VAR13,7,1)/SMA(VAR14,7,1)*100*VALID;
VAR16=SMA(VAR13,13,1)/SMA(VAR14,13,1)*100*VALID;
#历史至今的周期数
VAR17=COUNT(df.close.values!=None,0)-1;
VAR18=SMA(MAX(VAR12,0),6,1)/SMA(ABS(VAR12),6,1)*100*VALID;
VAR19=(-200)*(HHV(df.high.values,60)-df.close.values)/(HHV(df.high.values,60)-LLV(df.low.values,60))+100;
VAR1A=(df.close.values-LLV(df.low.values,15))/(HHV(df.high.values,15)-LLV(df.low.values,15))*100*VALID;
VAR1B=SMA((SMA(VAR1A,4,1)-50)*2,3,1)*VALID;
VAR1C=(INDEXC-LLV(INDEXL,14))/(HHV(INDEXH,14)-LLV(INDEXL,14))*100*VALID;
VAR1D=SMA(VAR1C,4,1)*VALID;
VAR1E=SMA(VAR1D,3,1)*VALID;
VAR1F=(HHV(df.high.values,30)-df.close.values)/df.close.values*100*VALID;
# VAR20=VAR18<=25 AND VAR19<-95 AND VAR1F>20 AND VAR1B<-30 AND VAR1E<30 AND VAR11A-df.close.values>=-0.25 AND VAR15<22 AND VAR16<28 AND VAR17>50;
VAR20=(VAR18<=25) & (VAR19<-95) & (VAR1F>20) & (VAR1B<-30) & (VAR1E<30) & (VAR11A-df.close.values>=-0.25) & (VAR15<22) & (VAR16<28) & (VAR17>50)
VAR21=(df.high.values+df.low.values+df.close.values)/3*VALID;
VAR22=(VAR21-MA(VAR21,14))/(0.015*AVEDEV(VAR21,14))*VALID;
VAR23=(VAR21-MA(VAR21,70))/(0.015*AVEDEV(VAR21,70))*VALID;
VAR24=IF((VAR22>=150) & (VAR22<200) & (VAR23>=150) & (VAR23<200),10,0);
VAR25=IF((VAR22<=-150) & (VAR22>-200) & (VAR23<=-150) & (VAR23>-200),-10,VAR24);
# STICKLINE(VAR20*VALID,0,37,3,0)*VALID,LINETHICK4,COLORLIMAGENTA;
# DRAWTEXT(CROSS(VAR20,0.5) AND COUNT(VAR20=cust_indicator,10)=cust_indicator,50,'超级建仓')*VALID , COLORLIMAGENTA;
VARE=MA(100*(df.close.values-LLV(df.close.values,34))/(HHV(df.high.values,34)-LLV(df.low.values,34)),5)-20;
VARF=100-3*SMA((df.close.values-LLV(df.low.values,75))/(HHV(df.high.values,75)-LLV(df.low.values,75))*100,20,1)+2*SMA(SMA
((df.close.values-LLV(df.low.values,75))/(HHV(df.high.values,75)-LLV(df.low.values,75))*100,20,1),15,1)*VALID;
VAR10=100-3*SMA((df.open.values-LLV(df.low.values,75))/(HHV(df.high.values,75)-LLV(df.low.values,75))*100,20,1)+2*SMA(SMA
((df.open.values-LLV(df.low.values,75))/(HHV(df.high.values,75)-LLV(df.low.values,75))*100,20,1),15,1)*VALID;
VAR11=(VARF<REF(VAR10,1)) & (df.volume.values>REF(df.volume.values,1)) & (df.close.values>REF(df.close.values,1)*VALID);
大资金=(VAR11*VALID) & (COUNT(VAR11,30)==1)
# DRAWTEXT(VAR11*VALID AND COUNT(VAR11,30)=cust_indicator*VALID,97*VALID,'大资金'),LINETHICK1,COLORFF00FF;
# STICKLINE(VAR11*VALID AND COUNT(VAR11,30)=cust_indicator,cust_indicator,85,2,0)*VALID,COLORFF00FF,LINETHICK4;
V1=(df.close.values*2+df.high.values+df.low.values)/4*10*VALID;
V2=EMA(V1,13)-EMA(V1,34)*VALID;
V3=EMA(V2,5);
V4=2*(V2-V3)*5.5;
V5=(HHV(INDEXH,8)-INDEXC)/(HHV(INDEXH,8)-LLV(INDEXL,8))*8*VALID;
V6=EMA(3*V5-2*SMA(V5,18,1),5);
V7=(INDEXC-LLV(INDEXL,8))/(HHV(INDEXH,8)-LLV(INDEXL,8))*10*VALID;
V8=(INDEXC*2+INDEXH+INDEXL)/4;
V9=EMA(V8,13)-EMA(V8,34)*VALID;
VA=EMA(V9,3)*VALID;
VB=(V9-VA)/2*VALID;
V11=3*SMA((df.close.values-LLV(df.low.values,55))/(HHV(df.high.values,55)-LLV(df.low.values,55))*100,5,1)-2*SMA(SMA((df.close.values-LLV(df.low.values,55))/(HHV(df.high.values,55)-LLV(df.low.values,55))*100,5,1),3,1)*VALID;
V12A=(EMA(V11,3)-REF(EMA(V11,3),1))/REF(EMA(V11,3),1)*100*VALID
BB= ((EMA(V11,3)<=13) & (V12A>13)) & FILTER(((EMA(V11,3)<=13) & (V12A>13)),10)*VALID;
CC=((EMA(V11,3)>=90) & (V12A>0)) & (FILTER(((EMA(V11,3)>=90) & (V12A>0)),10)*VALID);
DD=((EMA(V11,3)>=120) & (V12A>0)) & FILTER(((EMA(V11,3)>=120) & (V12A>0)),10)*VALID;
# STICKLINE(IF(VB>=0,VB*VALID,0)  AND EMA(V11,3)<13,0,20,3,0)*VALID,COLORBLUE;
# STICKLINE(IF(VB<=0,VB*VALID,0)  AND EMA(V11,3)>90,0,10,cust_indicator.5,0)*VALID,COLORGREEN;
# STICKLINE( IF(V4>=0,V4*VALID,cust_indicator) AND EMA(V11,3)<13,0,20,3,0)*VALID,COLORBLUE;
# STICKLINE(IF(V4<=0,V4*VALID,cust_indicator) AND EMA(V11,3)>90,0,10,cust_indicator.5,0)*VALID,COLORGREEN,LINETHICK1;
# DRAWTEXT (CC,22,'庄家逐步出货'),COLORGREEN;
# V10=PEAKBARS(3,15,cust_indicator)<10;
# V12=IF(V10==cust_indicator,50,0);
# 头部= IF(V12==50,100,0);
VAR200=(df.close.values-LLV(df.low.values,20))/(HHV(df.high.values,20)-LLV(df.low.values,20))*100*VALID;
VAR300=SMA(SMA(VAR200,3,1),3,1)/28.57;
VAR400=EMA(VAR300,5)*VALID;
VAR1G=(2*df.close.values+df.high.values+df.low.values+df.open.values)/5*VALID;
VAR2G=LLV(df.low.values,20)*VALID;
VAR3G=HHV(df.high.values,20)*VALID;
操盘=3*VAR300-2*VAR400*VALID;
PS1=(CROSS(操盘,VAR300)*VALID) & (VAR300<2.1) & (df.low.values>df.open.values)
上车柱=(CROSS(操盘,VAR300)*VALID) & (VAR300<2.1) & (df.close.values>df.open.values)
# STICKLINE(PS1*VALID,0,85,3,0)*VALID,COLORYELLOW;
# STICKLINE(PS1*VALID,0,5,2,0)*VALID,COLORYELLOW;
# DRAWTEXT(PS1*VALID,105,'上车'),COLORRED;
上车柱_1=CROSS(操盘,VAR300)*VALID
上车柱_2=VAR300<2.1
上车柱_3= df.close.values > df.open.values
print([上车柱==1])