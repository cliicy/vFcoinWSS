# Fcoin
fcoin


不定时在LTC\ETC等次热门币种抱团

依赖库:

pip install requests

pip install websocket_client==0.47.0

pip install numpy

pip install TA_Lib
pip install  -i https://pypi.tuna.tsinghua.edu.cn/simple TA_Lib
下载TA_Lib-0.4.17-cp36-cp36m-win_amd64.whl 然后安装

文件说明：

fcoin.py：修改自官方库

wss_app.py：WebSocket获取行情数据，REST私有API操作

config.py 配置文件，密匙在这里设置


接口api
https://developer.fcoin.com

内部git server:
http://10.0.131.49:10101/summary/quaninvest.git

How to run on Linux:
./run_fcoin.sh > fcoin_run.log 2>&1 &
