import backtrader as bt

class chipDistribution_indicator(bt.Indicator):
    lines = ('winner_line', 'cost_line')
    params = (
        ('minD', 0.01),
        ('flag', 1),
        ('AC', 1),
        ('N', 5),
        ('float_shares', 269600000000),#流通股本
        ('cost_pct', 90),
    )

    def __init__(self):
        self.Chip = {}
        self.ChipList = {}
        self.data = self.datas[0]

    def next(self):
        date = self.data.datetime.date(0).strftime('%Y-%m-%d')
        high = self.data.high[0]
        low = self.data.low[0]
        vol = self.data.volume[0]
        TurnoverRate = vol/self.p.float_shares
        avg = self.data.turnover[0]/ self.data.volume[0] if self.data.volume[0]!=0 else 0

        self.calcu(date, high, low, avg, vol, TurnoverRate, self.p.minD, self.p.flag, self.p.AC)
        self.lines.winner_line[0] = self.winner(self.data.close[0])
        self.lines.cost_line[0] = self.cost(self.p.cost_pct)

    def calcuJUN(self, dateT, highT, lowT, volT, TurnoverRateT, A, minD):

        x = []
        l = (highT - lowT) / minD
        for i in range(int(l)):
            x.append(round(lowT + i * minD, 2))
        length = len(x)
        eachV = volT / length if length!=0 else 0
        for i in self.Chip:
            self.Chip[i] = self.Chip[i] * (1 - TurnoverRateT * A)
        for i in x:
            if i in self.Chip:
                self.Chip[i] += eachV * (TurnoverRateT * A)
            else:
                self.Chip[i] = eachV * (TurnoverRateT * A)
        import copy
        self.ChipList[dateT] = copy.deepcopy(self.Chip)

    def calcuSin(self,dateT,highT, lowT,avgT, volT,TurnoverRateT,minD,A):
        x = []

        l = (highT - lowT) / minD
        for i in range(int(l)):
            x.append(round(lowT + i * minD, 2))
        # 计算仅仅今日的筹码分布
        tmpChip = {}


        # 极限法分割去逼近
        for i in x:
            x1 = i
            x2 = i + minD
            h = 2 / (highT - lowT) if highT - lowT!=0 else 0
            s = 0
            if i < avgT:
                y1 = h / (avgT - lowT) * (x1 - lowT) if (avgT - lowT) * (x1 - lowT)!=0 else 0
                y2 = h / (avgT - lowT) * (x2 - lowT) if (avgT - lowT) * (x2 - lowT)!=0 else 0
                s = minD * (y1 + y2) / 2
                s = s * volT
            else:
                y1 = h / (highT - avgT) * (highT - x1) if (highT - avgT) * (highT - x1) !=0 else 0
                y2 = h / (highT - avgT) * (highT - x2) if (highT - avgT) * (highT - x2)!=0 else 0

                s = minD * (y1 + y2) / 2
                s = s * volT
            tmpChip[i] = s

        for i in self.Chip:
            self.Chip[i] = self.Chip[i] * (1 - TurnoverRateT * A)

        for i in tmpChip:
            if i in self.Chip:
                self.Chip[i] += tmpChip[i] * (TurnoverRateT * A)
            else:
                self.Chip[i] = tmpChip[i] * (TurnoverRateT * A)
        import copy
        self.ChipList[dateT] = copy.deepcopy(self.Chip)

    def calcu(self, dateT, highT, lowT, avgT, volT, TurnoverRateT, minD=0.01, flag=1, AC=1):
        if flag == 1:
            self.calcuSin(dateT, highT, lowT, avgT, volT, TurnoverRateT, A=AC, minD=minD)
        elif flag == 2:
            self.calcuJUN(dateT,highT, lowT, volT, TurnoverRateT, A=AC, minD=minD)

    def winner(self, p):
        Profit = []
        Chip = self.ChipList[self.data.datetime.date(0).strftime('%Y-%m-%d')]
        total = 0
        be = 0
        for i in Chip:
            total += Chip[i]
            if i < p:
                be += Chip[i]
        if total != 0:
            bili = be / total
        else:
            bili = 0
        return bili

    def lwinner(self, N=5, p=None):
        data = self.datas[0].copy()
        date = data.datetime.date
        ans = []
        for i in range(len(date)):
            if i < N:
                ans.append(None)
                continue
            self.data = data.data[i - N:i]
            self.__init__()
            self.next()
            a = self.winner(p)
            ans.append(a)
        self.data = data
        return ans

    def cost(self, N):
        date = self.data.datetime.date(0).strftime('%Y-%m-%d')
        N = N / 100
        Chip = self.ChipList[date]

        ChipKey = sorted(Chip.keys())
        total = 0
        sumOf = 0
        for j in Chip:
            sumOf += Chip[j]

        for j in ChipKey:
            tmp = Chip[j]
            if sumOf != 0:
                tmp = tmp / sumOf
            total += tmp
            if total > N:
                return j
