import requests
import json

if __name__ == '__main__':
    # url='http://127.0.0.1:11111/hq/BasicQot'
    # kw = {
    #     'timeout_sec': 10,
    #     'params': {
    #         'security': [{
    #             'dataType': 10000,
    #             'code': '02439.HK'
    #         }]
    #     }
    # }
    # json_str = json.dumps(kw)
    # response=requests.post(url,data=json_str)
    # print(response.text)

    url='http://127.0.0.1:11111/hq/BasicQot'
    kw = {
        "timeout_sec": 10,
        "params": {
            "security": [{
                "dataType": "20000",
                "code": "TNXP"
            }],
            "needDelayFlag": "cust_indicator",
            "mktTmType": "-cust_indicator"
        }
    }
    json_str = json.dumps(kw)
    response=requests.post(url,data=json_str)
    print(response.text)