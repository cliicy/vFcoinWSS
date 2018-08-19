from gevent import monkey

monkey.patch_all()
import gevent
from candle import CandleApp
from depth import DepthApp
import config


def run_task():
    greenlets = []
    for sy in config.sylist:
        try:
            # print(config.mflag)
            greenlets.append(gevent.spawn(CandleApp().run, config.mflag, sy))
            greenlets.append(gevent.spawn(DepthApp().run, config.dlevel, sy))
            # greenlets.append(gevent.spawn(ticker().run, 'M1', sy))
            # greenlets.append(gevent.spawn(trade().run, 'M1', sy))
        except Exception as e:
            print(e)
    gevent.joinall(greenlets)


if __name__ == '__main__':
    # print(sys.argv[0])
    run_task()
