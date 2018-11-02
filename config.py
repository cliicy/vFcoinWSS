
#!-*-coding:utf-8 -*-
# @TIME    : 2018/7/26/0011 10:17
# @Author  : Luo
import os

# 秘钥
key = '55b6353945d14944bece3b5bc8d42580'
secret = 'e5f615e4d88d47a082a1b0f263fb8309'


trade_head = ['amount', 'ts', 'id', 'side', 'price']
# sylist = ['btcusdt', 'ethusdt', 'bchusdt', 'ltcusdt', 'ftusdt', 'fteth', 'etcusdt', 'ftbtc', 'bnbusdt', 'btmusdt']
sylist = ['btcusdt', 'bchusdt', 'ethusdt', 'ltcusdt', 'xrpusdt']
# sylist = ['btcusdt']
sD_ = '_data'
sD = '/yanjiuyuan/data' if os.environ.get("SHELL", "") else 'data'
exchange = 'fcoin'


# for ticker
tickerdir = 'ticker'


# for depthe
depthdir = 'depth'
dlevel = 'L20'

# for candle
klinedir = 'kline'
mflag = 'M1'
kline_interval = '1m'

# for trade
tradertdir = 'trader'

# for rabbitmq 1
# rabbitmq_host = "47.254.77.27"
# rabbitmq_username = "root"
# rabbitmq_pwd = "root"


# for rabbitmq 2
# rabbitmq_host = "172.24.132.207"
# rabbitmq_username = "guest"
# rabbitmq_pwd = "guest"

# for rabbitmq 2
#rabbitmq_host = "u217p36506.iok.la"
#rabbitmq_port = "37429"
#rabbitmq_username = "wuxiaobing"
#rabbitmq_pwd = "wuxiaobing"

rabbitmq_host = "51facai.51vip.biz"
rabbitmq_port = "50896"
rabbitmq_username = "guest"
rabbitmq_pwd = "guest"

emongodb = {
    "host": '172.24.132.208',
    "user": 'data',
    "password": 'data123',
    "db": 'invest',
    "port": '27017',
    "fcoin": 'fcoin'
}
