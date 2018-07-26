# !-*-coding:utf-8 -*-
# @TIME    : 2018/7/25/0011 15:32
# @Author  : Luo

import time
import logging
from threading import Thread

from fcoin import Fcoin
from WSS.fcoin_client import fcoin_client
import config
import os
import csv
import json
import sys
import subprocess

# sDir = os.path.join(os.path.abspath('..'), '..', 'Fcoin_DL')
sDir = os.path.join(os.path.abspath('..'), 'data')
depthdir = 'depth'
exchange = 'Fcoin'
dlevel = 'L20'


class MarketApp:
    """
    """

    def __init__(self):
        self.client = fcoin_client()
        self.fcoin = Fcoin()
        self.fcoin.auth(config.key, config.secret)
        self.sym = ''
        self._init_log()

    def depth(self, data):
        name, level, sym = self.client.channel_config[0].split('.')
        # print('symbol: ', sym)
        # create the no-exist folder to save date
        stime = time.strftime('%Y%m%d', time.localtime())
        depthDir = os.path.join(sDir, stime, exchange, depthdir)
        if not os.path.exists(depthDir):
            os.makedirs(depthDir)

        # 获取最新的深度明细
        # 买(卖)1价, 买(卖)1量
        depth_head = ['symbol', 'ts', 'depth', 'sell_price', 'buy_price', 'sell_amt', 'buy_amt']
        depth_flag = 'depth'

        # for original data
        sTfile = '{0}_{1}_{2}{3}'.format(depthdir, stime, sym, '.txt')
        sTfilepath = os.path.join(depthDir, sTfile)
        # for csv data
        dpfile = '{0}_{1}_{2}{3}'.format(depthdir, stime, sym, '.csv')
        dpspath = os.path.join(depthDir, dpfile)

        bidlists = data['bids']
        print(bidlists)
        asklists = data['asks']
        print(asklists)
        idp = 0
        nask = len(bidlists)
        rFind = False
        # depth_head = ['symbol', 'ts', 'depth', 'sell_price', 'buy_price', 'sell_amt', 'buy_amt']
        while idp < nask:
            if os.path.exists(dpspath):
                with open(dpspath, 'r', encoding='utf-8') as f:
                    first_line = f.readline()  # 取第一行
                    rFind = depth_flag in first_line
            with open(dpspath, 'a+', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                blst = bidlists[idp:idp + 2]
                alst = asklists[idp:idp + 2]
                balist = [sym, data['ts'], level, alst[0], blst[0], alst[1], blst[1]]
                # balist.extend(bidlists[idp:idp + 2])
                # balist.extend(asklists[idp:idp + 2])
                if rFind is True:
                    w.writerow(balist)
                    idp += 2
                else:
                    w.writerow(depth_head)
                    w.writerow(balist)
                    idp += 2
        f.close()

        # write original data to txt files
        with open(sTfilepath, 'a+', encoding='utf-8') as tf:
            tf.writelines(json.dumps(data) + '\n')
            tf.close()

    # 循环
    def loop(self):
        self.client.start()
        while not self.client.isConnected:
            self._log.info('waitting……')
            time.sleep(1)

        self.sync_depth(run.sym)
        while True:
            try:
                pass
            except Exception as error:
                print(error)
            time.sleep(1)

    # sync_trades
    def sync_depth(self, sym):
        self.client.stream.stream_depth.subscribe(self.depth)
        self.client.subscribe_depth(sym, dlevel)

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
    print('done')
