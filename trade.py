# !-*-coding:utf-8 -*-
# @TIME    : 2018/7/25/0011 15:32
# @Author  : Luo

import time
import logging
from threading import Thread

from fcoin import Fcoin
from WSS.fcoin_client import FcoinClient
import config
import os
import csv
import json
import sys

# sDir = os.path.join(os.path.abspath('..'), '..', 'Fcoin_DL')
sDir = os.path.join(os.path.abspath('..'), 'data')
tradertdir = 'trader'
exchange = 'Fcoin'


class MarketApp:
    """
    """

    def __init__(self):
        self.client = FcoinClient()
        self.fcoin = Fcoin()
        self.fcoin.auth(config.key, config.secret)
        self.sym = ''
        self._init_log()

    # write trade iformation
    def sync_tradesinfo(self, data):
        name, sym = self.client.channel_config[0].split('.')
        # print('symbol: ', sym)
        # create the no-exist folder to save date
        stime = time.strftime('%Y%m%d', time.localtime())
        stradeDir = os.path.join(sDir, stime, exchange, tradertdir)
        if not os.path.exists(stradeDir):
            os.makedirs(stradeDir)

        # for original data
        sTfile = '{0}_{1}_{2}{3}'.format(tradertdir, stime, sym, '.txt')
        sTfilepath = os.path.join(stradeDir, sTfile)

        sfile = '{0}_{1}_{2}{3}'.format(tradertdir, stime, sym, '.csv')
        sfilepath = os.path.join(stradeDir, sfile)
        sflag = 'price'
        rFind = False
        kklist = []
        vvlist = []
        if os.path.exists(sfilepath):
            with open(sfilepath, 'r', encoding='utf-8') as f:
                first_line = f.readline()  # 取第一行
                rFind = sflag in first_line
        with open(sfilepath, 'a+', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            if rFind is True:
                # vlist = list(data.values())
                vvlist.insert(0, sym)
                vvlist.insert(1, data["id"])
                vvlist.insert(2, data["ts"])
                vvlist.insert(3, data["side"])
                vvlist.insert(4, data["amount"])
                vvlist.insert(5, data["price"])
                w.writerow(vvlist)
            else:
                klist = list(data.keys())
                kklist.insert(0, 'symbol')
                kklist.insert(1, klist[2])
                kklist.insert(2, klist[1])
                kklist.insert(3, 'direction')
                kklist.insert(4, klist[0])
                kklist.insert(5, klist[4])
                w.writerow(kklist)
                vlist = list(data.values())
                vvlist.insert(0, sym)
                vvlist.insert(1, vlist[2])
                vvlist.insert(2, vlist[1])
                vvlist.insert(3, vlist[3])
                vvlist.insert(4, vlist[0])
                vvlist.insert(5, vlist[4])
                w.writerow(vvlist)
        f.close()

        # write original data to txt files
        with open(sTfilepath, 'a+', encoding='utf-8') as tf:
            tf.writelines(json.dumps(data) + '\n')
            tf.close()

    def trade(self, data):
        # print('数据：',data)
        self.sync_tradesinfo(data)

    # 循环
    def loop(self):
        self.client.start()

        while not self.client.isConnected:
            self._log.info('waitting……')
            time.sleep(1)

        self.sync_trades(self.sym)
        while True:
            try:
                pass
            except Exception as error:
                print(error)
            time.sleep(1)

    # sync_trades
    def sync_trades(self, sym):
        self.client.stream.stream_marketTrades.subscribe(self.trade)
        self.client.subscribe_trade(sym)

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
    print('done to get trade information data')
