from config import emongodb as mdb
from pymongo import MongoClient
mongo_url = 'mongodb://' + mdb["user"] + \
            ':' + mdb["password"] + '@' + mdb["host"] + ':' + \
            mdb["port"] + '/' + mdb["db"]
conn = MongoClient(mongo_url)
sdb = conn[mdb["db"]]
ybdd = {}

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
