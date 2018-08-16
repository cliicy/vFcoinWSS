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


sDir_ = os.path.join(os.path.abspath('..'), config.sD_)
sDir = os.path.join(os.path.abspath('..'), config.sD)

class MarketApp:
    """
    """
    def __init__(self):
        self.client = FcoinClient()
        self.fcoin = Fcoin()
        self.fcoin.auth(config.key, config.secret)
        self._sender = MqSender('fcoin', 'trade')
        self.sym = ''
        self.wdata = {}
        self._init_log()

    # write trade iformation
    def sync_tradesinfo(self, data):
        name, osym = self.client.channel_config[0].split('.')
        sym = Symbol.convert_to_standard_symbol(Platform.PLATFORM_FCOIN, osym)
        # send to mq
        if not self._sender:
            try:
                mqdata = {}
                tdata = {'symbol': sym, 'exchange': config.exchange}
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
        stradeDir = os.path.join(sDir, stime, config.exchange, config.tradertdir)
        # # for no-duplicated csv data
        if not os.path.exists(stradeDir):
            os.makedirs(stradeDir)
        ts = data['ts']
        # for original data
        sTfile = '{0}_{1}_{2}{3}'.format(config.tradertdir, stime, osym, '.txt')
        sTfilepath = os.path.join(stradeDir, sTfile)
        # write original data to txt files
        with open(sTfilepath, 'a+', encoding='utf-8') as tf:
            tf.writelines(json.dumps(data) + '\n')

        # for no-duplicated csv data
        sfile = '{0}_{1}_{2}{3}'.format(config.tradertdir, stime, osym, '.csv')
        sfilepath = os.path.join(stradeDir, sfile)
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
        self.w2csv(sfilepath, sym, data)

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

    def w2csv(self, sfilepath, sym, data):
        # will delete the data from the end if the ts is the same to the previous data
        iseekpos = self.wdata['wlen']
        # print('iseekpos= '+'{0}'.format(iseekpos))
        if iseekpos > 0:
            # print('will call deleteFromMmap')
            self.deleteFromMmap(sfilepath, iseekpos, 0, True)
        # will delete the data from the end if the ts is the same to the one of the previous data
        else:
            pass

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
        # update the lenth of data wroten to csv
        prelen = -1  # 多了一个逗号 所以从-1开始
        for item in vvlist:
            ss = '{0}{1}'.format(',', item)
            prelen += len(ss)
        prelen += len('\t\n')  # because there is a extra '\t\n' which is equal 2 bytes
        # print('w2csv prelen= ' + '{0}'.format(prelen))
        self.wdata['wlen'] = prelen
        # print('w2csv after prelen= ' + '{0}'.format(self.wdata['wlen']))
        # update the lenth of data wroten to csv

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
