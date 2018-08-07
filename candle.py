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
from sender import MqSender


sDir_ = os.path.join(os.path.abspath('..'), config.sD_)
sDir = os.path.join(os.path.abspath('..'), config.sD)
khead = ['symbol', 'ts', 'tm_intv', 'id', 'open', 'close', 'low', 'high', 'amount', 'vol', 'count']
dkey = ['id', 'open', 'close', 'low', 'high', 'quote_vol', 'base_vol', 'count']
m_interval = '1m'


class MarketApp:
    """
    """
    def __init__(self):
        self.client = FcoinClient()
        self.fcoin = Fcoin()
        self.fcoin.auth(config.key, config.secret)
        self._sender = MqSender('fcoin', 'kline')
        self.sym = ''
        self.wdata = {}
        self._init_log()

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

    def candle(self, data):
        # print('数据：', data)
        name, ml, sym = self.client.channel_config[0].split('.')
        ts = int(round(data['id'] * 1000))  # self.client.get_ts()
        # send to mq
        try:
            mqdata = {}
            tdata = {'symbol': sym, 'ts': ts, 'tm_intv': m_interval, 'exchange': config.exchange}
            mqdata.update(tdata)
            mqdata.update(data)
            # print(mqdata)
            self._sender.send(str(mqdata))
        except Exception as error:
            print(error)
            self._sender.close()
        # send to mq

        # print('symbol: ', sym)
        # create the no-exist folder to save date
        stime = time.strftime('%Y%m%d', time.localtime())
        stradeDir = os.path.join(sDir, stime, config.exchange, config.klinedir)
        if not os.path.exists(stradeDir):
            os.makedirs(stradeDir)

        # for original data
        sTfile = '{0}_{1}_{2}{3}'.format(config.klinedir, stime, sym, '.txt')
        sTfilepath = os.path.join(stradeDir, sTfile)
        # write original data to txt files
        with open(sTfilepath, 'a+', encoding='utf-8') as tf:
            tf.writelines(json.dumps(data) + '\n')
        # for no-duplicated csv data
        sfile = '{0}_{1}_{2}{3}'.format(config.klinedir, stime, sym, '.csv')
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
        self.w2csv(sfilepath, ts, sym, data)

    def w2csv(self, sfilepath, ts, sym, data):
        sflag = 'close'
        rFind = False
        kklist = []
        vvlist = []
        # will delete the data from the end if the ts is the same to the previous data
        iseekpos = self.wdata['wlen']
        # print('iseekpos= '+'{0}'.format(iseekpos))
        if iseekpos > 0:
            # print('will call deleteFromMmap')
            self.deleteFromMmap(sfilepath, iseekpos, 0, True)
        # will delete the data from the end if the ts is the same to the one of the previous data
        else:
            pass
        if os.path.exists(sfilepath):
            with open(sfilepath, 'r', encoding='utf-8') as f:
                first_line = f.readline()  # 取第一行
                rFind = sflag in first_line
        with open(sfilepath, 'a+', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            if rFind is True:
                vlist = list(data.values())
                self.additem2list(ts, vvlist, sym, m_interval, vlist)
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
                self.additem2list(ts, vvlist, sym, m_interval, vlist)
                w.writerow(vvlist)

        # update the lenth of data wroten to csv
        prelen = len('{0},{1},{2}'.format(sym, ts, m_interval))
        # print('prelen= ' + '{0}'.format(prelen))
        for i in dkey:
            ss = '{0}{1}'.format(',', data[i])
            prelen += len(ss)
        prelen += len('\t\n')  # because there is a extra '\t\n' which is equal 2 bytes
        # print('w2csv prelen= ' + '{0}'.format(prelen))
        self.wdata['wlen'] = prelen
        # print('w2csv after prelen= ' + '{0}'.format(self.wdata['wlen']))
        # update the lenth of data wroten to csv

    # add extral items to the original list
    def additem2list(self, ts, vvlist, sym, ml, vlist):
        self.sym = sym  # acutally it will not be used just for fix the warnning error
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
        self.client.subscribe_candle(sym, config.mflag)

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
