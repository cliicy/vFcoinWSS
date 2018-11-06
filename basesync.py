# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logging
import os
from config import kline_interval
import time
from fcoin import Fcoin
import config
import mmap
from config import sdb, mdb


fcoin = Fcoin()
fcoin.auth(config.key, config.secret)
sDir = os.path.join(os.path.abspath('..'), config.sD)


class BaseSync(object):
    def __init__(self, platform, data_type, interval):
        self.data_type = data_type
        self.platform = platform
        self.interval = interval
        # self._init_log()

    def run(self, *args):
        self.client.start()
        while not self.client.isConnected:
            self._log.info('waitting……')
            time.sleep(0.5)
        self.sync_data(*args)
        while True:
            try:
                pass
            except Exception as error:
                print(error)
            time.sleep(0.5)

    # add extral items to the original list
    # @staticmethod
    def additem2list(self, ts, vvlist, sym, ml, vitem):
        vvlist.insert(0, sym)
        vvlist.insert(1, ts)
        if ml == 'M1':  # when solution is M1, we will write 1m to csv
            ml = kline_interval
        vvlist.insert(2, ml)
        vvlist.insert(3, vitem['id'])
        vvlist.insert(4, vitem['open'])
        vvlist.insert(5, vitem['close'])
        vvlist.insert(6, vitem['low'])
        vvlist.insert(7, vitem['high'])
        vvlist.insert(8, vitem['quote_vol'])
        vvlist.insert(9, vitem['base_vol'])
        vvlist.insert(10, vitem['count'])

        # 把 下面的实时数据写入 Mongodb中
        # 'high' 最高价
        # 'low' 最低价
        # open 开盘价
        # close 收盘价
        # count
        # base_vol 基准货币成交量
        # quote_vol 计价货币成交量
        # 货币对
        ybdd = {}
        ybdd['sym'] = sym
        ybdd['_id'] = '{0}_{1}_{2}'.format(vitem['id'], vitem['seq'], vitem['quote_vol'])
        # 间隔时间
        ybdd['interval'] = ml
        # 开盘价格
        ybdd['open'] = vitem['open']
        # 最高价格
        ybdd['high'] = vitem['high']
        # 最低价
        ybdd['low'] = vitem['low']
        # 涨跌幅 Change 需要自己计算 或从网页爬取
        delta = '0.01'
        ybdd['Change'] = delta + '%'
        # close
        ybdd['close'] = vitem['close']
        # count
        ybdd['count'] = vitem['count']
        # quote_vol 计价货币成交量
        ybdd['quote_vol'] = round(vitem['quote_vol'], 2)
        ybdd['exchange'] = 'fcoin'
        ybdd['info_name'] = 'kline'
        coll = sdb[mdb[self.interval]]
        coll.insert(ybdd)

    # self.deleteFromMmap(sfilepath, size-iseekpos,size)
    @staticmethod
    def delline(filename, start, end, lastline=False):
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

    # 日志初始化
    def _init_log(self):
        self._log = logging.getLogger(__name__)
        self._log.setLevel(level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')  # 格式

        '''
        保存文档
        '''
        handler = logging.FileHandler("appFcoin.log")
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

