# !-*-coding:utf-8 -*-
# @TIME    : 2018/7/25/0011 15:32
# @Author  : Luo

import time
import logging
from threading import Thread
import pandas as pd
from fcoin import Fcoin
from WSS.fcoin_client import FcoinClient
import config
import os
import csv
import json
import sys

sDir_ = os.path.join(os.path.abspath('..'), '_data')
sDir = os.path.join(os.path.abspath('..'), 'data')
klinedir = 'kline'
exchange = 'fcoin'
mflag = 'M1'
khead = ['symbol', 'ts', 'tm_intv', 'id', 'open', 'close', 'low', 'high', 'amount', 'vol', 'count']


class MarketApp:
    """
    """

    def __init__(self):
        self.client = FcoinClient()
        self.fcoin = Fcoin()
        self.fcoin.auth(config.key, config.secret)
        self.sym = ''
        self.oldts = ''
        self.wdata = {}
        self.bwrite = False
        self._init_log()

    def candle(self, data):
        # print('数据：',data)
        name, ml, sym = self.client.channel_config[0].split('.')
        ts = self.client.get_ts()
        # print('symbol: ', sym)
        # create the no-exist folder to save date
        stime = time.strftime('%Y%m%d', time.localtime())
        stDir = os.path.join(sDir_, stime, exchange, klinedir)
        stradeDir = os.path.join(sDir, stime, exchange, klinedir)
        if not os.path.exists(stradeDir):
            os.makedirs(stradeDir)

        if not os.path.exists(stDir):
            os.makedirs(stDir)

        # for original data
        sTfile = '{0}_{1}_{2}{3}'.format(klinedir, stime, sym, '.txt')
        sTfilepath = os.path.join(stradeDir, sTfile)

        sfile = '{0}_{1}_{2}{3}'.format(klinedir, stime, sym, '.csv')
        stfilepath = os.path.join(stDir, sfile)

        sfile = '{0}_{1}_{2}{3}'.format(klinedir, stime, sym, '.csv')
        sfilepath = os.path.join(stradeDir, sfile)

        sflag = 'close'
        rFind = False
        kklist = []
        vvlist = []
        if os.path.exists(stfilepath):
            with open(stfilepath, 'r', encoding='utf-8') as f:
                first_line = f.readline()  # 取第一行
                rFind = sflag in first_line
        with open(stfilepath, 'a+', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            if rFind is True:
                vlist = list(data.values())
                self.additem2list(ts, vvlist, sym, '1m', vlist)
                w.writerow(vvlist)
            else:  # khead = ['symbol', 'ts', 'tm_intv', 'id', 'open', 'close', 'low', 'high', 'amount', 'vol', 'count']
                klist = list(data.keys())
                # open,close,high,quote_vol,id,count,low,seq,base_vol
                kklist.insert(0, 'symbol')
                kklist.insert(1, 'ts')
                kklist.insert(2, 'tm_intv')
                kklist.insert(3, klist[4])
                kklist.insert(4, klist[0])
                kklist.insert(5, klist[1])
                kklist.insert(6, klist[6])
                kklist.insert(7, klist[2])
                kklist.insert(8, 'amount')
                kklist.insert(9, 'vol')
                kklist.insert(10, klist[5])
                w.writerow(kklist)
                vlist = list(data.values())
                self.additem2list(ts, vvlist, sym, '1m', vlist)
                w.writerow(vvlist)
        f.close()

        # use pandas to remove duplicate data
        df = pd.read_csv(stfilepath)
        df = df.drop_duplicates(['ts'], keep='last')
        df.to_csv(sfilepath, index=False)

        # write original data to txt files
        with open(sTfilepath, 'a+', encoding='utf-8') as tf:
            tf.writelines(json.dumps(data) + '\n')
            tf.close()

    # add extral items to the original list
    def additem2list(self, ts, vvlist, sym, ml, vlist):
        self.sym = sym  # acutally it will not be used
        vvlist.insert(0, sym)
        vvlist.insert(1, ts)
        vvlist.insert(2, ml)
        vvlist.insert(3, vlist[4])
        vvlist.insert(4, vlist[0])
        vvlist.insert(5, vlist[1])
        vvlist.insert(6, vlist[6])
        vvlist.insert(7, vlist[2])
        vvlist.insert(8, vlist[3])
        vvlist.insert(9, vlist[8])
        vvlist.insert(10, vlist[5])

    # 循环
    def loop(self):
        self.client.start()

        while not self.client.isConnected:
            self._log.info('waitting……')
            time.sleep(1)

        self.sync_kline(self.sym)
        while True:
            try:
                pass
            except Exception as error:
                print(error)
            time.sleep(1)

    # sync_trades
    def sync_kline(self, sym):
        self.client.stream.stream_klines.subscribe(self.candle)
        self.client.subscribe_candle(sym, mflag)

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
    run.sym = sys.argv[1]
    thread = Thread(target=run.loop)
    thread.start()
    thread.join()
    print('kline finished')
