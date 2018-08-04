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

sDir_ = os.path.join(os.path.abspath('..'), config.sD_)
sDir = os.path.join(os.path.abspath('..'), config.sD)


class MarketApp:
    """
    """
    def __init__(self):
        self.client = FcoinClient()
        self.fcoin = Fcoin()
        self.fcoin.auth(config.key, config.secret)
        self._sym = ''
        self.wdata = {}
        self._init_log()

    def ticker(self, data):
        name, sym = self.client.channel_config[0].split('.')
        ts = self.client.get_ts()
        # print('symbol: ', sym)
        # create the no-exist folder to save date
        stime = time.strftime('%Y%m%d', time.localtime())
        tickerDir = os.path.join(sDir, stime, config.exchange, config.tickerdir)
        if not os.path.exists(tickerDir):
            os.makedirs(tickerDir)

        # for original data
        sTfile = '{0}_{1}_{2}{3}'.format(config.tickerdir, stime, sym, '.txt')
        sTfilepath = os.path.join(tickerDir, sTfile)
        # write original data to txt files
        with open(sTfilepath, 'a+', encoding='utf-8') as tf:
            tf.writelines(json.dumps(data) + '\n')
            tf.close()

        # for no-duplicated csv data
        tkfile = '{0}_{1}_{2}{3}'.format(config.tickerdir, stime, sym, '.csv')
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
            self.deleteFromMmap(tspath, iseekpos, 0, True)
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

    # self.deleteFromMmap(sfilepath, size-iseekpos,size)
    def deleteFromMmap(self, filename, start, end, lastline=False):
        self._sym = self._sym  # acutally it will not be used just for fix the warnning error
        f = open(filename, "r+")
        VDATA = mmap.mmap(f.fileno(), 0)
        size = len(VDATA)
        if lastline is True:
            start = size - start
            end = size
        else:
            pass
        length = end - start
        newsize = size - length
        VDATA.move(start, end, size - end)
        VDATA.flush()
        VDATA.close()
        f.truncate(newsize)
        f.close()

    # 循环
    def loop(self):
        self.client.start()
        while not self.client.isConnected:
            self._log.info('waitting……')
            time.sleep(1)

        self.sync_ticker(self._sym)
        while True:
            try:
                pass
            except Exception as error:
                print(error)
            time.sleep(1)

    # sync_trades
    def sync_ticker(self, sym):
        self.client.stream.stream_ticker.subscribe(self.ticker)
        self.client.subscribe_ticker(sym)

    # add extral items to the original list
    # ['symbol', 'ts', 'latest_price', 'latest_amount', 'max_buy1_price', 'max_buy1_amt',
    #        'min_sell1_price', 'min_sell1_amt', 'pre_24h_price', 'pre_24h_price_max', 'pre_24h_price_min',
    #        'pre_24h_bt_finish_amt', 'pre_24h_usd_finish_amt']
    # 最新成交价,最近一笔成交的成交量,最大买一价,最大买一量,最小卖一价,最小卖一量,24小时前成交价,24小时内最高价,
    # 24小时内最低价,24小时内基准货币成交量,24小时内计价货币成交量
    def addI2list(self, ts, vvlist, sym, vlist):
        self._sym = sym  # acutally it will not be used
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

    # 日志初始化
    def _init_log(self):
        self._log = logging.getLogger(__name__)
        self._log.setLevel(level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')  # 格式

        '''
        保存文档
        '''
        handler = logging.FileHandler("app.log")
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        self._log.addHandler(handler)

        '''
        控制台显示
        '''
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        self._log.addHandler(console)


if __name__ == '__main__':
    run = MarketApp()
    run._sym = sys.argv[1]
    thread = Thread(target=run.loop)
    thread.start()
    thread.join()
    print('ticker finished')
