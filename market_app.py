# !-*-coding:utf-8 -*-
# @TIME    : 2018/7/21/0011 15:32
# @Author  : Luo

import logging
from multiprocessing import Process
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

    def loop(self):
        self._log
        # create 4 processes to get depth data parallelly
        for sy in config.sylist:
            pdepth = Process(target=do_depth, args=(sy,))
            print('syncing depth information will start.')
            pdepth.start()

            ptrade = Process(target=do_trades, args=(sy,))
            print('syncing trades information will start.')
            ptrade.start()

            pkline = Process(target=do_kline, args=(sy,))
            print('syncing kline information will start.')
            pkline.start()

            pticker = Process(target=do_ticker, args=(sy,))
            print('syncing ticker information will start.')
            pticker.start()


if __name__ == '__main__':
    run = MarketApp()
    run.loop()
    print('done to trigger depth ticker kline trades')
