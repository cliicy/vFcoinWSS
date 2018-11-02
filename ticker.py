# !-*-coding:utf-8 -*-
# @TIME    : 2018/7/25/0011 15:32
# @Author  : Luo

import time
import logging
from threading import Thread
import mmap
from fcoin import Fcoin
from WSS.fcoin_client import FcoinClient
import config
import os
import csv
import json
import sys
from sender import MqSender
from enums import Symbol
from enums import Platform
from basesync import BaseSync
from enums import PlatformDataType
from basesync import sDir

from config import emongodb as mdb
from pymongo import MongoClient
mongo_url = 'mongodb://' + mdb["user"] + \
            ':' + mdb["password"] + '@' + mdb["host"] + ':' + \
            mdb["port"] + '/' + mdb["db"]
conn = MongoClient(mongo_url)
sdb = conn[mdb["db"]]
ybdd = {}


class TickerApp(BaseSync):
    """
    """
    def __init__(self):
        self.platform = Platform.PLATFORM_FCOIN.value
        self.data_type = PlatformDataType.PLATFORM_DATA_TICKER.value
        BaseSync(self.platform, self.data_type)
        self.client = FcoinClient()
        self._init_log()
        self._sender = MqSender('3', 'ticker')
        self.wdata = {}

    def ticker(self, data):
        name, osym = self.client.channel_config[0].split('.')
        sym = Symbol.convert_to_standard_symbol(Platform.PLATFORM_FCOIN, osym)
        # ts = self.client.get_ts()
        # 从服务器得到的数据中没有ts，也没有id，根据文档要求，要把获取到数据的时间存入csv文件及数据库中
        ts = int(round(time.time() * 1000))
        # send to mq
        if self._sender is not None:
            try:
                mqdata = {}
                tdata = {'symbol': sym, 'ts': ts, 'exchange': config.exchange}
                mqdata.update(tdata)
                mqdata.update(data)
                # print(mqdata)
                self._sender.send(str(mqdata))
            except Exception as error:
                print(error)
                self._sender.close()
        else:
            # print('fail to connect rabbitmq server')
            pass
        # send to mq

        # print('symbol: ', sym)
        # create the no-exist folder to save date
        stime = time.strftime('%Y%m%d', time.localtime())
        tickerDir = os.path.join(sDir, stime, config.exchange, config.tickerdir)
        if not os.path.exists(tickerDir):
            os.makedirs(tickerDir)

        # for original data
        sTfile = '{0}_{1}_{2}{3}'.format(config.tickerdir, stime, osym, '.txt')
        sTfilepath = os.path.join(tickerDir, sTfile)
        # write original data to txt files
        with open(sTfilepath, 'a+', encoding='utf-8') as tf:
            tf.writelines(json.dumps(data) + '\n')

        # for no-duplicated csv data
        tkfile = '{0}_{1}_{2}{3}'.format(config.tickerdir, stime, osym, '.csv')
        tspath = os.path.join(tickerDir, tkfile)

        if self.wdata:
            if ts in self.wdata.values():
                # self.wdata['ts'] = ts
                pass
            else:
                self.wdata['ts'] = ts
                self.wdata['wlen'] = 0
            # write the current data sent from server to the csv but the position will be changed
        else:
            self.wdata['ts'] = ts
            self.wdata['wlen'] = 0
        self.w2csv(tspath, ts, sym, data)

    def w2csv(self, tspath, ts, sym, data):
        # will delete the data from the end if the ts is the same to the previous data
        iseekpos = self.wdata['wlen']
        # print('iseekpos= '+'{0}'.format(iseekpos))
        if iseekpos > 0:
            # print('will call deleteFromMmap')
            self.delline(tspath, iseekpos, 0, True)
        # will delete the data from the end if the ts is the same to the one of the previous data
        else:
            pass

        # 获取最新的深度明细
        ticker_head = []
        ticker_flag = 'latest_price'

        tklist = []
        rFind = False
        if os.path.exists(tspath):
            with open(tspath, 'r', encoding='utf-8') as f:
                first_line = f.readline()  # 取第一行
                rFind = ticker_flag in first_line
        with open(tspath, 'a+', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            if rFind is True:
                self.addI2list(ts, tklist, sym, data['ticker'])
                w.writerow(tklist)
            else:
                ticker_head.insert(0, 'symbol')
                ticker_head.insert(1, 'ts')
                ticker_head.insert(2, 'latest_price')
                ticker_head.insert(3, 'latest_amount')
                ticker_head.insert(4, 'max_buy1_price')
                ticker_head.insert(5, 'max_buy1_amt')
                ticker_head.insert(6, 'min_sell1_price')
                ticker_head.insert(7, 'min_sell1_amt')
                ticker_head.insert(8, 'pre_24h_price')
                ticker_head.insert(9, 'pre_24h_price_max')
                ticker_head.insert(10, 'pre_24h_price_min')
                ticker_head.insert(11, 'pre_24h_bt_finish_amt')
                ticker_head.insert(12, 'pre_24h_usd_finish_amt')
                w.writerow(ticker_head)
                self.addI2list(ts, tklist, sym, data['ticker'])
                w.writerow(tklist)
        # update the lenth of data wroten to csv
        prelen = len('{0},{1}'.format(sym, ts))
        # print('prelen= ' + '{0}'.format(prelen))
        for i in range(11):
            ss = '{0}{1}'.format(',', data['ticker'][i])
            prelen += len(ss)
        prelen += len('\t\n')  # because there is a extra '\t\n' which is equal 2 bytes
        # print('w2csv prelen= ' + '{0}'.format(prelen))
        self.wdata['wlen'] = prelen
        # print('w2csv after prelen= ' + '{0}'.format(self.wdata['wlen']))
        # update the lenth of data wroten to csv

    # sync_trades
    def sync_data(self, *args):
        self.client.stream.stream_ticker.subscribe(self.ticker)
        self.client.subscribe_ticker(args[0])

    # add extral items to the original list
    # ['symbol', 'ts', 'latest_price', 'latest_amount', 'max_buy1_price', 'max_buy1_amt',
    #        'min_sell1_price', 'min_sell1_amt', 'pre_24h_price', 'pre_24h_price_max', 'pre_24h_price_min',
    #        'pre_24h_bt_finish_amt', 'pre_24h_usd_finish_amt']
    # 最新成交价,最近一笔成交的成交量,最大买一价,最大买一量,最小卖一价,最小卖一量,24小时前成交价,24小时内最高价,
    # 24小时内最低价,24小时内基准货币成交量,24小时内计价货币成交量
    @staticmethod
    def addI2list(ts, vvlist, sym, vlist):
        vvlist.insert(0, sym)
        vvlist.insert(1, ts)
        vvlist.insert(2, vlist[0])
        vvlist.insert(3, vlist[1])
        vvlist.insert(4, vlist[2])
        vvlist.insert(5, vlist[3])
        vvlist.insert(6, vlist[4])
        vvlist.insert(7, vlist[5])
        vvlist.insert(8, vlist[6])
        vvlist.insert(9, vlist[7])
        vvlist.insert(10, vlist[8])
        vvlist.insert(11, vlist[9])
        vvlist.insert(12, vlist[10])

        # 把 下面的实时数据写入 Mongodb中
        # 'latest_price' 最新成交价
        # pre_24h_price_max 24小时内最高价
        # pre_24h_price_min 24小时内最低价
        # pre_24h_usd_finish_amt 24小时内计价货币成交量
        # 货币对
        ybdd['sym'] = sym
        # 价格 Price  latest_price
        ybdd['Price'] = vlist[0]
        # 涨跌幅 Change 需要自己计算 或从网页爬取
        delta = '0.11'
        ybdd['Change'] = delta + '%'

        # High  pre_24h_price_max 24小时内最高价
        ybdd['High'] = vlist[7]

        # Low pre_24h_price_min 24小时内最低价
        ybdd['High'] = vlist[8]

        # Volume pre_24h_usd_finish_amt 24小时内计价货币成交量
        ybdd['Volume'] = vlist[10]

        dfcoin_coll = sdb[mdb["fcoin"]]
        dfcoin_coll.update({'Change': ybdd['Change'], 'Price': ybdd['Price'], 'Volume': ybdd['Volume']},
                           {'$set': ybdd}, True)


if __name__ == '__main__':
    run = TickerApp()
    run._sym = sys.argv[1]
    thread = Thread(target=run.run)
    thread.start()
    thread.join()
    print('ticker finished')
