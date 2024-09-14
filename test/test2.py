from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse

import backtrader as bt
import backtrader.feeds as btfeeds

import pandas as pd
import json
import requests

def get_data():
    url = 'http://127.0.0.1:11111/hq/KL'
    kw = {
        "timeout_sec": 10,
        "params": {
            "security": {
                "dataType": "10000",
                "code": "02439.HK"
            },
            "startDate": "20240101",
            "direction": "cust_indicator",
            "exRightFlag": "2",
            "cycType": "2",
            "limit": "500"
        }
    }
    json_str = json.dumps(kw)
    response = requests.post(url, data=json_str)
    return pd.read_json(json.dumps(json.loads(response.text)['data']['kline'])).set_index('date').rename(columns={'closePrice': 'close', 'highPrice': 'high', 'openPrice': 'open', 'volume': 'volume'})


def runstrat():
    args = parse_args()

    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=False)

    # Add a strategy
    cerebro.addstrategy(bt.Strategy)


    dataframe =get_data()

    if not args.noprint:
        print('--------------------------------------------------')
        print(dataframe)
        print('--------------------------------------------------')

    data = bt.feeds.PandasData(dataname=dataframe)

    cerebro.adddata(data)

    # Run over everything
    cerebro.run()

    # Plot the result
    cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pandas test script')

    parser.add_argument('--noheaders', action='store_true', default=False,
                        required=False,
                        help='Do not use header rows')

    parser.add_argument('--noprint', action='store_true', default=False,
                        help='Print the dataframe')

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()