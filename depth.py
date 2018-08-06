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
import mmap
sDir_ = os.path.join(os.path.abspath('..'), config.sD_)
sDir = os.path.join(os.path.abspath('..'), config.sD)


class MarketApp:
    """
    """
    def __init__(self):
        self.client = FcoinClient()
        self.fcoin = Fcoin()
        self.fcoin.auth(config.key, config.secret)
        self.sym = ''
        self.wdata = {}
        self._init_log()

    def depth(self, data):
        name, level, sym = self.client.channel_config[0].split('.')
        # print('symbol: ', sym)
        # create the no-exist folder to save date
        stime = time.strftime('%Y%m%d', time.localtime())
        ts = data['ts']
        depthDir = os.path.join(sDir, stime, config.exchange, config.depthdir)
        if not os.path.exists(depthDir):
            os.makedirs(depthDir)

        # for original data
        sTfile = '{0}_{1}_{2}{3}'.format(config.depthdir, stime, sym, '.txt')
        sTfilepath = os.path.join(depthDir, sTfile)
        # write original data to txt files
        with open(sTfilepath, 'a+', encoding='utf-8') as tf:
            tf.writelines(json.dumps(data) + '\n')

        # for no-duplicated csv data
        dpfile = '{0}_{1}_{2}{3}'.format(config.depthdir, stime, sym, '.csv')
        dpspath = os.path.join(depthDir, dpfile)
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
        self.w2csv(dpspath, sym, data, level)

    # 循环
    def loop(self):
        self.client.start()
        while not self.client.isConnected:
            self._log.info('waitting……')
            time.sleep(1)

        self.sync_depth(self.sym)
        while True:
            try:
                pass
            except Exception as error:
                print(error)
            time.sleep(1)

    # sync_trades
    def sync_depth(self, sym):
        self.client.stream.stream_depth.subscribe(self.depth)
        self.client.subscribe_depth(sym, config.dlevel)

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

    # self.deleteFromMmap(sfilepath, size-iseekpos,size)
    def deleteFromMmap(self, filename, start, end, lastline=False):
        self.sym = self.sym  # acutally it will not be used just for fix the warnning error
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

    def w2csv(self, sfilepath, sym, data, level):
        # 获取最新的深度明细
        # 买(卖)1价, 买(卖)1量
        # 显示列名
        depth_head = ['symbol', 'ts', 'depth', 'sell_price', 'buy_price', 'sell_amt', 'buy_amt']
        depth_flag = 'depth'
        # 存放要写入CVSV的数据data
        balist = []
        # will delete the data from the end if the ts is the same to the previous data
        iseekpos = self.wdata['wlen']
        # print('iseekpos= '+'{0}'.format(iseekpos))
        if iseekpos > 0:
            # print('will call deleteFromMmap')
            self.deleteFromMmap(sfilepath, iseekpos, 0, True)
        # will delete the data from the end if the ts is the same to the one of the previous data
        else:
            pass
        bidlists = data['bids']
        # print(bidlists)
        asklists = data['asks']
        # print(asklists)
        # iloops = 0
        idp = 0
        nask = len(bidlists)
        rFind = False
        # depth_head = ['symbol', 'ts', 'depth', 'sell_price', 'buy_price', 'sell_amt', 'buy_amt']
        level = int(level.lstrip('L'))
        # print('{0}'.format(level))
        while idp < nask:
            if os.path.exists(sfilepath):
                with open(sfilepath, 'r', encoding='utf-8') as f:
                    first_line = f.readline()  # 取第一行
                    rFind = depth_flag in first_line
            with open(sfilepath, 'a+', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                blst = bidlists[idp:idp + 2]
                alst = asklists[idp:idp + 2]
                idepth = 1 + idp / 2
                balist = [sym, data['ts'], idepth, alst[0], blst[0], alst[1], blst[1]]
                # balist.extend(bidlists[idp:idp + 2])
                # balist.extend(asklists[idp:idp + 2])
                if rFind is True:
                    # if idepth == level:  # only write the depthest data to csv
                    w.writerow(balist)
                    idp += 2
                else:
                    w.writerow(depth_head)
                    # if idepth == level:  # only write the depthest data to csv
                    w.writerow(balist)
                    idp += 2

        # update the lenth of data wroten to csv
        prelen = -1  # 多了一个逗号 所以从-1开始
        # print('prelen= ' + '{0}'.format(prelen))
        for item in balist:
            ss = '{0}{1}'.format(',', item)
            prelen += len(ss)
        prelen += len('\t\n')  # because there is a extra '\t\n' which is equal 2 bytes
        # print('w2csv prelen= ' + '{0}'.format(prelen))
        self.wdata['wlen'] = prelen
        # print('w2csv after prelen= ' + '{0}'.format(self.wdata['wlen']))
        # update the lenth of data wroten to csv


if __name__ == '__main__':
    run = MarketApp()
    run.sym = sys.argv[1]
    thread = Thread(target=run.loop)
    thread.start()
    thread.join()
    print('done')
