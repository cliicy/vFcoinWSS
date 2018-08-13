
#!-*-coding:utf-8 -*-
# @TIME    : 2018/7/26/0011 10:17
# @Author  : Luo
import os

# 秘钥
key = '55b6353945d14944bece3b5bc8d42580'
secret = 'e5f615e4d88d47a082a1b0f263fb8309'


# 精度和最小挂单量
btc = {'name': 'btcusdt', 'coin': 'btc', 'price_precision': 2, 'amount_precision': 4, 'min_amount': 0.001}
bch = {'name': 'bchusdt', 'coin': 'bch', 'price_precision': 2, 'amount_precision': 4, 'min_amount': 0.001}
ltc = {'name': 'ltcusdt', 'coin': 'ltc', 'price_precision': 2, 'amount_precision': 4, 'min_amount': 0.001}
eth = {'name': 'ethusdt', 'coin': 'eth', 'price_precision': 2, 'amount_precision': 4, 'min_amount': 0.001}
etc = {'name': 'etcusdt', 'coin': 'etc', 'price_precision': 2, 'amount_precision': 4, 'min_amount': 0.001}
ft = {'name': 'ftusdt', 'coin': 'ft', 'price_precision': 6, 'amount_precision': 0, 'min_amount': 5}
btm = {'name': 'btmusdt', 'coin': 'btm', 'price_precision': 4, 'amount_precision': 1, 'min_amount': 5}

# 交易对，仅支持以上USDT交易对
symbol = ft

# 抱团模式：固定价格刷单(等于0就是市价，大于0固定该价格)
fix_price = 0

# 当固定价格有效时,买入前判断市价与固定价的差价，在范围帐内则下单
diff_price = 0.02

# ★买卖深度前3挂单数量总和
total_amount = 0

# 当★满足时的买入挂单量,如果梭哈刷设置个很大的值
max_amount = 6

# 当★不满足时的买入挂单量
min_amount = 6

# 持仓币种最大量
limit_amount = 10

# 暂时无用
ft_base_amount = 0

# 买单超时(s)
delay = 20

trade_head = ['amount', 'ts', 'id', 'side', 'price']
# sylist = ['btcusdt', 'ethusdt', 'bchusdt', 'ltcusdt', 'ftusdt', 'fteth', 'etcusdt', 'ftbtc', 'bnbusdt', 'btmusdt']
sylist = ['btcusdt', 'bchusdt', 'ethusdt', 'ltcusdt']
# sylist = ['btcusdt']
sD_ = '_data'
sD = '/data' if os.environ.get("SHELL", "") else 'data'
exchange = 'fcoin'


# for ticker
tickerdir = 'ticker'


# for depthe
depthdir = 'depth'
dlevel = 'L20'

# for candle
klinedir = 'kline'
mflag = 'M1'

# for trade
tradertdir = 'trader'

# for rabbitmq
rabbitmq_host = "172.24.132.207"
rabbitmq_username = "guest"
rabbitmq_pwd = "guest"
