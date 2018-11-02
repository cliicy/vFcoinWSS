from config import emongodb as mdb
from pymongo import MongoClient
import time
import pandas as pd

mongo_url = 'mongodb://' + mdb["user"] + \
            ':' + mdb["password"] + '@' + mdb["host"] + ':' + \
            mdb["port"] + '/' + mdb["db"]
conn = MongoClient(mongo_url)
sdb = conn[mdb["db"]]
coll = sdb[mdb["fcoin"]]
ybdd = {}


def t_update():
    # 把 下面的实时数据写入 Mongodb中
    # 'latest_price' 最新成交价
    # pre_24h_price_max 24小时内最高价
    # pre_24h_price_min 24小时内最低价
    # pre_24h_usd_finish_amt 24小时内计价货币成交量
    # 货币对
    ybdd['sym'] = 'aa'
    # 价格 Price  latest_price
    ybdd['Price'] = '6666'
    # 涨跌幅 Change 需要自己计算 或从网页爬取
    delta = '0.11'
    ybdd['Change'] = delta + '%'

    # High  pre_24h_price_max 24小时内最高价
    ybdd['High'] = '8888'

    # Low pre_24h_price_min 24小时内最低价
    ybdd['Low'] = '2222'

    # Volume pre_24h_usd_finish_amt 24小时内计价货币成交量
    ybdd['Volume'] = '0'

    dfcoin_coll = sdb[mdb["fcoin"]]
    # dfcoin_coll.update({'Change': ybdd['Change'], 'Price': ybdd['Price'], 'Volume': ybdd['Volume']},
    #                    {'$set': ybdd}, True)
    dfcoin_coll.update({'sym': ybdd['sym']}, {'$set': {'Change': ybdd['Change'], 'High': ybdd['High'],
                                                       'Low': ybdd['Low'], 'Volume': ybdd['Volume']}}, True)


ticker = []
# ones = {}


def notify():
    dd = {'ticker': ticker}

    while True:
        try:
            data = pd.DataFrame(list(coll.find()))
            data = data[['sym', 'Change', 'High', 'Low', 'Price', 'Volume']]
            dc = data.set_index('sym').T.to_dict('dict')
            for k, vdata in dc.items():
                tk = {}
                tk['数字货币'] = k
                tk['最新价'] = vdata['Price']
                tk['涨跌幅'] = vdata['Change']
                tk['成交量'] = vdata['Volume']
                tk['24小时内最高价'] = vdata['High']
                tk['24小时内最低价'] = vdata['Low']
                # ones.update(tk)
                ticker.append(tk)
            # print(data.to_string(index=False))
            # print(ticker)
        except Exception as error:
            print(error)
        time.sleep(30)
    # dfcoin_coll = sdb[mdb["fcoin"]]
    # # watchCursor = db.getSiblingDB("data").sensors.watch(
    # #     [],
    # #     {fullDocument: "updateLookup"}
    # # )
    # change_stream = dfcoin_coll.watch([
    #     {'$match': {
    #         'operationType': {'$in': ['insert', 'replace']}
    #     }}
    # ])
    # for change in change_stream:
    #     print(change)

    # sdb.createCollection("log", {capped: True, size: 100000})
    # dfcoin_coll = sdb[mdb["fcoin"]]
    # cursor = dfcoin_coll.find(tailable=True)
    # while cursor.alive:
    #     try:
    #         doc = cursor.next()
    #         print(doc)
    #     except StopIteration:
    #         time.sleep(1)


if __name__ == '__main__':
    notify()

