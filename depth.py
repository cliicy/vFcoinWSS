# !-*-coding:utf-8 -*-
# @TIME    : 2018/7/25/0011 15:32
# @Author  : Luo

import time
from basesync import sDir
from threading import Thread
from basesync import BaseSync
from WSS.fcoin_client import FcoinClient
import config
import os
import csv
import json
import sys
from sender import MqSender
from enums import Symbol
from enums import Platform
from enums import PlatformDataType


class DepthApp(BaseSync):
    """
    """
    def __init__(self):

        self.platform = Platform.PLATFORM_FCOIN.value
        self.data_type = PlatformDataType.PLATFORM_DATA_DEPTH.value
        BaseSync(self.platform, self.data_type)
        self.client = FcoinClient()
        self._init_log()
        self._sender = MqSender('fcoin', 'depth')
        self.wdata = {}

    def depth(self, data):
        # print(data)
        name, level, osym = self.client.channel_config[0].split('.')
        sym = Symbol.convert_to_standard_symbol(Platform.PLATFORM_FCOIN, osym)
        # send to mq
        if not self._sender:
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
        else:
            # print('fail to connect rabbitmq server')
            pass
        # send to mq
        # print('symbol: ', sym)
        # create the no-exist folder to save date
        stime = time.strftime('%Y%m%d', time.localtime())
        ts = data['ts']
        depthDir = os.path.join(sDir, stime, config.exchange, config.depthdir)
        if not os.path.exists(depthDir):
            os.makedirs(depthDir)

        # for original data
        sTfile = '{0}_{1}_{2}{3}'.format(config.depthdir, stime, osym, '.txt')
        sTfilepath = os.path.join(depthDir, sTfile)
        # write original data to txt files
        with open(sTfilepath, 'a+', encoding='utf-8') as tf:
            tf.writelines(json.dumps(data) + '\n')

        # for no-duplicated csv data
        dpfile = '{0}_{1}_{2}{3}'.format(config.depthdir, stime, osym, '.csv')
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

    # sync_trades
    def sync_data(self, *args):
        self.client.stream.stream_depth.subscribe(self.depth)
        self.client.subscribe_depth(args[1], args[0])

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
            self.delline(sfilepath, iseekpos, 0, True)
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
    run = DepthApp()
    run.sym = sys.argv[1]
    thread = Thread(target=run.run)
    thread.start()
    thread.join()
    print('done')
