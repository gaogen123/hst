


import copy

import baostock as bs
import pandas as pd


class ChipDistribution():

    def __init__(self):
        self.Chip = {} # 当前获利盘
        self.ChipList = {}  # 所有的获利盘的
        self.data= pd.DataFrame({})

    def get_data(self,code,start_date, end_date):



        #### 登陆系统 ####
        lg = bs.login()
        # 显示登陆返回信息
        # print('login respond error_code:'+lg.error_code)
        # print('login respond  error_msg:'+lg.error_msg)
        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs = bs.query_history_k_data_plus(code,
                                          "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                          start_date=start_date, end_date=end_date,
                                          frequency="d", adjustflag="3")
        # print('query_history_k_data_plus respond error_code:'+rs.error_code)
        # print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        #### 结果集输出到csv文件 ####
        # result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
        # print(result)

        #### 登出系统 ####
        bs.logout()


        data1=result.rename(columns={"amount":"money","turn":"TurnoverRate"})
        data1=data1[['volume','open','high','low','close','money','date','TurnoverRate']]
        data1['avg']=data1['money'].astype(float)/data1['volume'].astype(int)
        # data1['avg'] = np.divide(data1['money'].astype(float), data1['volume'].astype(int), out=np.zeros_like(data1['money'].astype(float)), where=data1['volume'].astype(int) != 0)
        data1['TurnoverRate']=data1['TurnoverRate'].astype(float)
        data1['volume']=data1['volume'].astype(int)
        data1['open']=data1['open'].astype(float)
        data1['high']=data1['high'].astype(float)
        data1['low']=data1['low'].astype(float)
        data1['close']=data1['close'].astype(float)
        data1['money']=data1['money'].astype(float)

        self.data=data1
        # volume, open, high, low, close, money, avg, date, TurnoverRate
        # 成交量，开盘价，最高价，最低价，收盘价，成交额，均价（成交额/成交量），日期，换手率
        # self.data = pd.read_csv('test.csv')


    def calcuJUN(self,dateT,highT, lowT, volT, TurnoverRateT, A, minD):

        x =[]
        l = (highT - lowT) / minD if minD!=0 else 0
        for i in range(int(l)):
            x.append(round(lowT + i * minD, 2))
        length = len(x)
        eachV = volT/length if length!=0 else 0
        for i in self.Chip:
            self.Chip[i] = self.Chip[i] *(1 -TurnoverRateT * A)
        for i in x:
            if i in self.Chip:
                self.Chip[i] += eachV *(TurnoverRateT * A)
            else:
                self.Chip[i] = eachV *(TurnoverRateT * A)
        import copy
        self.ChipList[dateT] = copy.deepcopy(self.Chip)



    def calcuSin(self,dateT,highT, lowT,avgT, volT,TurnoverRateT,minD,A):
        x =[]

        l = (highT - lowT) / minD if minD!=0 else 0
        for i in range(int(l)):
            x.append(round(lowT + i * minD, 2))
        #计算仅仅今日的筹码分布
        tmpChip = {}
        #极限法分割去逼近
        for i in x:
            x1 = i
            x2 = i + minD
            h = 2 / (highT - lowT) if highT - lowT!=0 else 0
            s= 0
            if i < avgT:
                y1 = h /(avgT - lowT) * (x1 - lowT) if (avgT - lowT) * (x1 - lowT)!=0 else 0
                y2 = h /(avgT - lowT) * (x2 - lowT) if (avgT - lowT) * (x2 - lowT)!=0 else 0
                s = minD *(y1 + y2) /2
                s = s * volT
            else:
                y1 = h /(highT - avgT) *(highT - x1) if (highT - avgT) *(highT - x1)!=0 else 0
                y2 = h /(highT - avgT) *(highT - x2) if (highT - avgT) *(highT - x2)!=0 else 0

                s = minD *(y1 + y2) /2
                s = s * volT
            tmpChip[i] = s


        for i in self.Chip:
            self.Chip[i] = self.Chip[i] *(1 -TurnoverRateT * A)

        for i in tmpChip:
            if i in self.Chip:
                self.Chip[i] += tmpChip[i] *(TurnoverRateT * A)
            else:
                self.Chip[i] = tmpChip[i] *(TurnoverRateT * A)
        import copy
        self.ChipList[dateT] = copy.deepcopy(self.Chip)


    def calcu(self,dateT,highT, lowT,avgT, volT, TurnoverRateT,minD = 0.01, flag=1 , AC=1):
        if flag ==1:
            self.calcuSin(dateT,highT, lowT,avgT, volT, TurnoverRateT,A=AC, minD=minD)
        elif flag ==2:
            self.calcuJUN(dateT,highT, lowT, volT, TurnoverRateT, A=AC, minD=minD)

    def calcuChip(self, flag=1, AC=1):  #flag 使用哪个计算方式,    AC 衰减系数
        low = self.data['low']
        high = self.data['high']
        vol = self.data['volume']
        TurnoverRate = self.data['TurnoverRate']
        avg = self.data['avg']
        date = self.data['date']

        for i in range(len(date)):
        #     if i < 90:
        #         continue

            highT = high[i]
            lowT = low[i]
            volT = vol[i]
            TurnoverRateT = TurnoverRate[i]
            avgT = avg[i]
            # print(date[i])
            dateT = date[i]
            self.calcu(dateT,highT, lowT,avgT, volT, TurnoverRateT/100, flag=flag, AC=AC)  # 东方财富的小数位要注意，兄弟萌。我不除100懵逼了

        # 计算winner
    def winner(self,p=None):
            Profit = []
            date = self.data['date']

            if p == None:  # 不输入默认close
                p = self.data['close']
                count = 0
                for i in self.ChipList:
                    # 计算目前的比例
                    Chip = self.ChipList[i]
                    total = 0
                    be = 0
                    for i in Chip:
                        total += Chip[i]
                        if i < p[count]:
                            be += Chip[i]
                    if total != 0:
                        bili = be / total if total!=0 else 0
                    else:
                        bili = 0
                    count += 1
                    Profit.append(bili)
            else:
                for i in self.ChipList:
                    # 计算目前的比例

                    Chip = self.ChipList[i]
                    total = 0
                    be = 0
                    for i in Chip:
                        total += Chip[i]
                        if i < p:
                            be += Chip[i]
                    if total != 0:
                        bili = be / total if total!=0 else 0
                    else:
                        bili = 0
                    Profit.append(bili)

            # import matplotlib.pyplot as plt
            # plt.plot(date[len(date) - 200:-cust_indicator], Profit[len(date) - 200:-cust_indicator])
            # plt.show()

            return Profit

    def lwinner(self,N = 5, p=None):

        data = copy.deepcopy(self.data)
        date = data['date']
        ans = []
        for i in range(len(date)):
            # print(date[i])
            if i < N:
                ans.append(None)
                continue
            self.data = data[i-N:i]
            self.data.index= range(0,N)
            self.__init__()
            self.calcuChip()    #使用默认计算方式
            a = self.winner(p)
            ans.append(a[-1])
        import matplotlib.pyplot as plt
        plt.plot(date[len(date) - 60:-1], ans[len(date) - 60:-1])
        plt.show()

        self.data = data
        return ans



    def cost(self,N):
        date = self.data['date']

        N = N / 100  # 转换成百分比
        ans = []
        for i in self.ChipList:  # 我的ChipList本身就是有顺序的
            Chip = self.ChipList[i]
            ChipKey = sorted(Chip.keys())  # 排序
            total = 0  # 当前比例
            sumOf = 0  # 所有筹码的总和
            for j in Chip:
                sumOf += Chip[j]

            for j in ChipKey:
                tmp = Chip[j]
                tmp = tmp / sumOf if sumOf!=0 else 0
                total += tmp
                if total > N:
                    ans.append(j)
                    break
        import matplotlib.pyplot as plt
        plt.plot(date[len(date) - 1000:-1], ans[len(date) - 1000:-1])
        plt.show()
        return ans



if __name__ == "__main__":
    a=ChipDistribution()
    code='sh.600084'
    a.get_data(code,'2022-07-19', '2024-05-31')  #获取数据
    a.calcuChip(flag=1, AC=1) #计算
    a.winner() #获利盘
    a.cost(90) #成本分布



    a.lwinner()
