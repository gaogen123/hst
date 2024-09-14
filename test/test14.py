import yfinance as yf

def get_float_shares(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return info.get('floatShares')

# 使用示例
float_shares = get_float_shares("AAPL")  # 获取苹果公司的流通股本
print(f"Float shares: {float_shares}")
