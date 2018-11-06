from gevent import monkey

monkey.patch_all()
import gevent
from candle import CandleApp
from D1Candle import D1CandleApp
from H1candle import H1CandleApp
from M5candle import M5CandleApp
from W1Candle import W1CandleApp
from depth import DepthApp
from ticker import TickerApp
from trade import TradeApp
import config


def run_task():
    greenlets = []
    for sy in config.sylist:
        try:
            # print(config.mflag)
            greenlets.append(gevent.spawn(CandleApp().run, config.mflag, sy))
            greenlets.append(gevent.spawn(M5CandleApp().run, 'M5', sy))
            greenlets.append(gevent.spawn(D1CandleApp().run, 'D1', sy))
            greenlets.append(gevent.spawn(H1CandleApp().run, 'H1', sy))
            greenlets.append(gevent.spawn(W1CandleApp().run, 'W1', sy))
            greenlets.append(gevent.spawn(DepthApp().run, config.dlevel, sy))
            greenlets.append(gevent.spawn(TickerApp().run, sy))
            greenlets.append(gevent.spawn(TradeApp().run, sy))
        except Exception as e:
            print(e)
    gevent.joinall(greenlets)


if __name__ == '__main__':
    # print(sys.argv[0])
    run_task()
