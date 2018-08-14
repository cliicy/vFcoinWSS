#! /bin/bash


nohup python candle.py btcusdt > /dev/null 2>&1 &
nohup python candle.py bchusdt > /dev/null 2>&1 &
nohup python candle.py ethusdt > /dev/null 2>&1 &
nohup python candle.py ltusdt > /dev/null 2>&1 &
nohup python ticker.py btcusdt > /dev/null 2>&1 &
nohup python ticker.py bchusdt > /dev/null 2>&1 &
nohup python ticker.py ethusdt > /dev/null 2>&1 &
nohup python ticker.py ltcusdt > /dev/null 2>&1 &
nohup python depth.py btcusdt > /dev/null 2>&1 &
nohup python depth.py bchusdt > /dev/null 2>&1 &
nohup python depth.py ethusdt > /dev/null 2>&1 &
nohup python depth.py ltusdt > /dev/null 2>&1 &
nohup python trade.py btcusdt > /dev/null 2>&1 &
nohup python trade.py bchusdt > /dev/null 2>&1 &
nohup python trade.py ethusdt > /dev/null 2>&1 &
nohup python trade.py ltcusdt > /dev/null 2>&1 &

