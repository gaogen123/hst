import akshare as ak
import pandas as pd


def get_sh_stocks(top_n=3):
    # 获取所有A股列表
    stock_info_a_code_name_df = ak.stock_info_a_code_name()

    # 筛选出上证股票（股票代码以60开头）
    sh_stocks = stock_info_a_code_name_df[stock_info_a_code_name_df['code'].str.startswith('60')]

    # 按照股票代码排序
    # sh_stocks_sorted = sh_stocks.sort_values('code')

    return sh_stocks.head(top_n)


def get_stock_info(code):
    # 获取个股基本面数据
    stock_info = ak.stock_individual_info_em(symbol=code)
    return stock_info


# 获取前3个上证股票
top_stocks = get_sh_stocks(3)

print("上证前3个股票信息：")
for _, stock in top_stocks.iterrows():
    code = stock['code']
    name = stock['name']

    info = get_stock_info(code)
    if not info.empty:
        print(f"\n股票代码: {code}")
        print(f"股票名称: {name}")
    else:
        print(f"\n无法获取 {code} 的详细信息")

