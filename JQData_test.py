# 导入技术分析指标库
from jqdatasdk import *
from jqdatasdk.technical_analysis import *

auth('18626194472','Rnu@0#rr') #账号是申请时所填写的手机号；密码为聚宽官网登录密码

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']


# 计算并输出 security_list1 的 GDX 值，分别返回：济安线、压力线和支撑线的值。
gdx_jax, gdx_ylx, gdx_zcx = GDX(security_list1,check_date='2023-03-02', N = 30, M = 9)
print (gdx_jax[security_list1])
print (gdx_ylx[security_list1])
print (gdx_zcx[security_list1])

# 输出 security_list2 的 GDX 值
gdx_jax, gdx_ylx, gdx_zcx = GDX(security_list2,check_date='2023-03-02', N = 30, M = 9)
for stock in security_list2:
    print (gdx_jax[stock])
    print (gdx_ylx[stock])
    print (gdx_zcx[stock])
