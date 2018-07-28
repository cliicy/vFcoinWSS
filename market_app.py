# !-*-coding:utf-8 -*-
# @TIME    : 2018/7/21/0011 15:32
# @Author  : Luo

import time
import logging
from collections import defaultdict
from threading import Thread
from multiprocessing import Process
from fcoin import Fcoin
from WSS.fcoin_client import fcoin_client
import config
import subprocess


def do_trades(sym):
    cmd = '{0}{1}'.format('python trade.py ', sym)
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    print(pipe.read())
    print('finished to get trades information')


def do_depth(sym):
    cmd = '{0}{1}'.format('python depth.py ', sym)
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    print(pipe.read())
    print('finished to get depth information')


def do_kline(sym):
    cmd = '{0}{1}'.format('python candle.py ', sym)
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    print(pipe.read())
    print('finished to get kline information')


def do_ticker(sym):
    cmd = '{0}{1}'.format('python ticker.py ', sym)
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    print(pipe.read())
    print('finished to get ticker information')


class MarketApp:
    def __init__(self):
        self.client = fcoin_client()
        self.fcoin = Fcoin()
        self.fcoin.auth(config.key, config.secret)
        self.ts = None  # 深度更新时间
        self.market_price = None  # 市价
        self.market_trade_list = None
        self.total_bids = 0
        self.total_asks = 0
        self.filled_buy_order_list = []
        self.order_list = defaultdict(lambda: None)
        self.buy_order_id = None
        self.dic_balance = defaultdict(lambda: None)
        self.time_order = time.time()
        #
        self.price_list = []
        self.candle_list = []
        self.SMA = None
        self._init_log()

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

    # 循环
    def loop(self):
        self.client.start()
        while not self.client.isConnected:
            self._log.info('waitting……')
            time.sleep(1)

        # create 4 processes to get depth data parallelly
        for sy in config.sylist:
            p = Process(target=do_depth, args=(sy,))
            print('syncing depth information will start.')
            p.start()

        # create 4 processes to get trades data parallelly
        for sy in config.sylist:
            # self.do_trades(sy)
            p = Process(target=do_trades, args=(sy,))
            print('syncing trades information will start.')
            p.start()

        # create 4 processes to get kline data parallelly
        for sy in config.sylist:
            p = Process(target=do_kline, args=(sy,))
            print('syncing kline information will start.')
            p.start()

        # create 4 processes to get ticker data parallelly
        for sy in config.sylist:
            p = Process(target=do_ticker, args=(sy,))
            print('syncing ticker information will start.')
            p.start()


if __name__ == '__main__':
    run = MarketApp()
    thread = Thread(target=run.loop)
    thread.start()
    thread.join()
    print('done to trigger depth ticker kline trades')
