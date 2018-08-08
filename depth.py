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


class MarketApp:
    """
    """
    def __init__(self):
        self.client = FcoinClient()
        self.fcoin = Fcoin()
        self.fcoin.auth(config.key, config.secret)
        self._sender = MqSender('fcoin', 'depth')
        self.sym = ''
        self.wdata = {}
        self._init_log()

    def depth(self, data):
        name, level, sym = self.client.channel_config[0].split('.')
        # level = 'L20'
        # sym = 'btcusdt'
        # send to mq
        try:
            mqdata = {}
            tdata = {'symbol': sym, 'level': level, 'exchange': config.exchange}
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
        idp = 0
        nask = len(bidlists)
        rFind = False
        # depth_head = ['symbol', 'ts', 'depth', 'sell_price', 'buy_price', 'sell_amt', 'buy_amt']
        level = int(level.lstrip('L'))
        # print('{0}'.format(level))
        nwdatalen = 0
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

                # update the lenth of data wroten to csv
                prelen = -1  # 多了一个逗号 所以从-1开始
                for item in balist:
                    ss = '{0}{1}'.format(',', item)
                    # print('depth数据=', ss.strip())
                    prelen += len(ss)
                nwdatalen += prelen
                nwdatalen += len('\t\n')
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

        self.wdata['wlen'] = nwdatalen
        # update the lenth of data wroten to csv


if __name__ == '__main__':
    # trun = MarketApp()
    # data1 = {"bids": [6519.49, 0.0118, 6519.46, 0.03, 6519.14, 0.06, 6518.21, 0.0012, 6517.53, 0.03, 6515.57, 0.0275, 6515.04, 0.0012, 6514.47, 0.2606, 6514.3, 0.0012, 6514.2, 0.004, 6513.66, 0.03, 6513.65, 0.03, 6513.64, 0.03, 6513.63, 0.03, 6512.24, 0.01, 6512.23, 0.0121, 6512.18, 0.6, 6511.71, 0.03, 6509.77, 0.0567, 6509.76, 0.03], "asks": [6521.92, 0.0115, 6522.96, 0.003, 6523.38, 0.01, 6523.42, 0.003, 6524.66, 0.003, 6525.28, 0.0012, 6525.34, 0.03, 6525.88, 0.0001, 6527.3, 0.0387, 6527.79, 0.003, 6528.3, 0.0012, 6529.26, 0.09, 6529.39, 0.003, 6529.43, 0.0121, 6529.49, 0.003, 6529.75, 0.003, 6529.83, 0.0012, 6529.96, 0.006, 6530.53, 0.26, 6530.77, 0.003], "ts": 1533710558007, "seq": 169519420}
    # data2 = {"bids": [6519.49, 0.0118, 6519.46, 0.03, 6519.14, 0.06, 6518.21, 0.0012, 6517.53, 0.03, 6515.57, 0.0275, 6515.04, 0.0012, 6514.47, 0.2606, 6514.3, 0.0012, 6514.2, 0.004, 6513.66, 0.03, 6513.65, 0.03, 6513.64, 0.03, 6513.63, 0.03, 6512.24, 0.01, 6512.23, 0.0121, 6512.18, 0.6, 6511.71, 0.03, 6509.77, 0.0567, 6509.76, 0.03], "asks": [6521.92, 0.0115, 6522.96, 0.003, 6523.38, 0.01, 6523.42, 0.003, 6524.66, 0.003, 6525.28, 0.0012, 6525.34, 0.03, 6525.88, 0.0001, 6527.3, 0.0387, 6527.79, 0.003, 6528.3, 0.0012, 6529.26, 0.09, 6529.39, 0.003, 6529.43, 0.0121, 6529.49, 0.003, 6529.75, 0.003, 6529.83, 0.0012, 6529.96, 0.006, 6530.53, 0.26, 6530.77, 0.003], "ts": 1533710558007, "seq": 169519420}
    # trun.depth(data1)
    # trun.depth(data2)
    run = MarketApp()
    run.sym = sys.argv[1]
    thread = Thread(target=run.loop)
    thread.start()
    thread.join()
    print('done')
