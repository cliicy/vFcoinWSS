# !-*-coding:utf-8 -*-
# @TIME    : 2018/7/25/0011 15:32
# @Author  : Luo
import time
from basesync import sDir
from threading import Thread
import config
import os
import csv
import sys
from sender import MqSender
from enums import Symbol
from enums import Platform
from basesync import BaseSync
from enums import PlatformDataType
from WSS.fcoin_client import FcoinClient

khead = ['symbol', 'ts', 'tm_intv', 'id', 'open', 'close', 'low', 'high', 'amount', 'vol', 'count']
dkey = ['id', 'open', 'close', 'low', 'high', 'quote_vol', 'base_vol', 'count']


class D1CandleApp(BaseSync):
    """
    """
    def __init__(self):
        self.platform = Platform.PLATFORM_FCOIN.value
        self.data_type = PlatformDataType.PLATFORM_DATA_KLINE.value
        self.interval = 'D1'
        BaseSync(self.platform, self.data_type, self.interval)
        self.client = FcoinClient()
        self._init_log()
        self._sender = MqSender('3', 'kline')
        # self._sender = MqSender('fcoin', 'kline')
        self.wdata = {}

    def candle(self, data):
        # print('数据：', data)
        name, ml, osym = self.client.channel_config[0].split('.')
        sym = Symbol.convert_to_standard_symbol(Platform.PLATFORM_FCOIN, osym)
        ts = int(round(data['id'] * 1000))  # self.client.get_ts()
        # 从服务器得到的数据中没有ts，只有id，根据文档要求，要把获取到数据的时间存入csv文件及数据库中
        ticks = ts  # int(round(time.time() * 1000))
        data['id'] = ts
        # print("当前时间戳为:", ticks)
        # send to mq
        # if self._sender is not None:
        #     try:
        #         mqdata = {}
        #         tdata = {'symbol': sym, 'ts': ticks, 'tm_intv': m_interval, 'exchange': config.exchange}
        #         mqdata.update(tdata)
        #         mqdata.update(data)
        #         # print(mqdata)
        #         self._sender.send(str(mqdata))
        #     except Exception as error:
        #         print(error)
        #         self._sender.close()
        # else:
        #     # print('fail to connect rabbitmq server')
        #     pass
        # send to mq

        # print('symbol: ', sym)
        # create the no-exist folder to save date
        stime = time.strftime('%Y%m%d', time.localtime())
        skldir = os.path.join(sDir, stime, config.exchange, config.klinedir)
        if not os.path.exists(skldir):
            os.makedirs(skldir)
        # for original data
        # sTfile = '{0}_{1}_{2}_{3}{4}'.format(config.klinedir, stime, ml, osym, '.txt')
        # sTfilepath = os.path.join(skldir, sTfile)
        # # write original data to txt files
        # with open(sTfilepath, 'a+', encoding='utf-8') as tf:
        #     tf.writelines(json.dumps(data) + '\n')
        # for no-duplicated csv data
        sfile = '{0}_{1}_{2}_{3}{4}'.format(config.klinedir, stime, ml, osym, '.csv')
        sfilepath = os.path.join(skldir, sfile)
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
        self.w2csv(sfilepath, ticks, sym, data)  # 是要把ticks写入csv,而不是和id值一致的ts

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
            self.delline(sfilepath, iseekpos, 0, True)
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
                # vlist = list(data.values())
                self.additem2list(ts, vvlist, sym, self.interval, data)
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
                self.additem2list(ts, vvlist, sym, self.interval, data)
                w.writerow(vvlist)

        # update the lenth of data wroten to csv
        prelen = len('{0},{1},{2}'.format(sym, ts, self.interval))
        # print('prelen= ' + '{0}'.format(prelen))
        for i in dkey:
            ss = '{0}{1}'.format(',', data[i])
            prelen += len(ss)
        prelen += len('\t\n')  # because there is a extra '\t\n' which is equal 2 bytes
        # print('w2csv prelen= ' + '{0}'.format(prelen))
        self.wdata['wlen'] = prelen
        # print('w2csv after prelen= ' + '{0}'.format(self.wdata['wlen']))
        # update the lenth of data wroten to csv

    def sync_data(self, *args):
        self.client.stream.stream_klines.subscribe(self.candle)
        self.client.subscribe_candle(args[1], args[0])


if __name__ == '__main__':
    print('kline main')
    run = D1CandleApp()
    run.sym = sys.argv[1]
    thread = Thread(target=run.run)
    thread.start()
    thread.join()
    print('kline finished')
