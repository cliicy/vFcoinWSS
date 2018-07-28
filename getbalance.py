#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Luo
"""
import os
import time
import json
from fcoin import Fcoin
import csv
import config

sDir = os.path.join(os.path.abspath('..'), 'data')
exchange = 'Fcoin'
depositdir = 'balance'


def getbalance():
    """
    获取当前账户信息：
    :return:
    """
    print("取得当前账户信息： ")
    fcoin = Fcoin()
    fcoin.auth(config.key, config.secret)
    rdata = fcoin.get_balance()
    bainfo = rdata[1]['data']
    # create the no-exist folder to save date
    stime = time.strftime('%Y%m%d', time.localtime())
    balDir = os.path.join(sDir, stime, exchange, depositdir)
    if not os.path.exists(balDir):
        os.makedirs(balDir)

    # for original data
    sTfile = '{0}_{1}{2}'.format(stime, 'balance', '.txt')
    sTfilepath = os.path.join(balDir, sTfile)
    # write original data to txt files
    with open(sTfilepath, 'a+', encoding='utf-8') as tf:
        tf.writelines(json.dumps(rdata) + '\n')
        tf.close()

    # # for csv data
    balfile = '{0}_{1}{2}'.format(stime, 'balance', '.csv')
    balpath = os.path.join(balDir, balfile)
    sflag = 'balance'
    rFind = False
    for item in bainfo:
        if rFind is False and os.path.exists(balpath):
            with open(balpath, 'r', encoding='utf-8') as f:
                first_line = f.readline()  # 取第一行
                rFind = sflag in first_line
        with open(balpath, 'a+', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            if rFind is True:
                vlist = list(item.values())
                w.writerow(vlist)
            else:
                klist = list(item.keys())
                w.writerow(klist)
                vlist = list(item.values())
                w.writerow(vlist)
    f.close()


if __name__ == '__main__':
    getbalance()
