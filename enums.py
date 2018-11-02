#  -*- coding:utf-8 -*-
from enum import Enum, unique


@unique
class Platform(Enum):
    """
    交易平台枚举
    """
    PLATFORM_HUOBI = "1"
    PLATFORM_BINANCE = "2"
    PLATFORM_FCOIN = "3"
    PLATFORM_OKEX = "5"
    PLATFORM_OKEX_FUTURE = "4"


@unique
class PlatformDataType(Enum):
    """
    交易平台数据类型
    """
    PLATFORM_DATA_KLINE = "kline"
    PLATFORM_DATA_TICKER = "ticker"
    PLATFORM_DATA_TRADE = "trade"
    PLATFORM_DATA_DEPTH = "depth"


@unique
class PlatformDataTypeIndex(Enum):
    """
    交易平台数据类型序号枚举
    """
    HUOBI_KLINE_DB_INDEX = 1
    HUOBI_TICKER_DB_INDEX = 2
    HUOBI_TRADE_DB_INDEX = 3
    HUOBI_DEPTH_DB_INDEX = 4
    BINANCE_KLINE_DB_INDEX = 5
    BINANCE_TICKER_DB_INDEX = 6
    BINANCE_TRADE_DB_INDEX = 7
    BINANCE_DEPTH_DB_INDEX = 8
    FCOIN_KLINE_DB_INDEX = 9
    FCOIN_TICKER_DB_INDEX = 10
    FCOIN_TRADE_DB_INDEX = 11
    FCOIN_DEPTH_DB_INDEX = 12
    OKEX_KLINE_DB_INDEX = 13
    OKEX_TICKER_DB_INDEX = 14
    OKEX_TRADE_DB_INDEX = 15
    OKEX_DEPTH_DB_INDEX = 16
    OKEX_FUTURE_KLINE_DB_INDEX = 17
    OKEX_FUTURE_TICKER_DB_INDEX = 18
    OKEX_FUTURE_TRADE_DB_INDEX = 19
    OKEX_FUTURE_DEPTH_DB_INDEX = 20

    @staticmethod
    def getIndex(platform, data_type):
        """
        根据平台和数据类型返回编号
        :param platform:
        :param data_type:
        :return:
        """
        if platform == Platform.PLATFORM_HUOBI.value:
            """火币"""
            if data_type == PlatformDataType.PLATFORM_DATA_KLINE.value:
                return PlatformDataTypeIndex.HUOBI_KLINE_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_TICKER.value:
                return PlatformDataTypeIndex.HUOBI_TICKER_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_TRADE.value:
                return PlatformDataTypeIndex.HUOBI_TRADE_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_DEPTH.value:
                return PlatformDataTypeIndex.HUOBI_DEPTH_DB_INDEX.value
        elif platform == Platform.PLATFORM_BINANCE.value:
            """币安"""
            if data_type == PlatformDataType.PLATFORM_DATA_KLINE.value:
                return PlatformDataTypeIndex.BINANCE_KLINE_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_TICKER.value:
                return PlatformDataTypeIndex.BINANCE_TICKER_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_TRADE.value:
                return PlatformDataTypeIndex.BINANCE_TRADE_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_DEPTH.value:
                return PlatformDataTypeIndex.BINANCE_DEPTH_DB_INDEX.value
        elif platform == Platform.PLATFORM_FCOIN.value:
            """FCOIN"""
            if data_type == PlatformDataType.PLATFORM_DATA_KLINE.value:
                return PlatformDataTypeIndex.FCOIN_KLINE_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_TICKER.value:
                return PlatformDataTypeIndex.FCOIN_TICKER_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_TRADE.value:
                return PlatformDataTypeIndex.FCOIN_TRADE_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_DEPTH.value:
                return PlatformDataTypeIndex.FCOIN_DEPTH_DB_INDEX.value
        elif platform == Platform.PLATFORM_OKEX.value:
            """OKEX"""
            if data_type == PlatformDataType.PLATFORM_DATA_KLINE.value:
                return PlatformDataTypeIndex.OKEX_KLINE_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_TICKER.value:
                return PlatformDataTypeIndex.OKEX_TICKER_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_TRADE.value:
                return PlatformDataTypeIndex.OKEX_TRADE_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_DEPTH.value:
                return PlatformDataTypeIndex.OKEX_DEPTH_DB_INDEX.value
        elif platform == Platform.PLATFORM_OKEX_FUTURE.value:
            """OKEX合约"""
            if data_type == PlatformDataType.PLATFORM_DATA_KLINE.value:
                return PlatformDataTypeIndex.OKEX_FUTURE_KLINE_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_TICKER.value:
                return PlatformDataTypeIndex.OKEX_FUTURE_TICKER_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_TRADE.value:
                return PlatformDataTypeIndex.OKEX_FUTURE_TRADE_DB_INDEX.value
            elif data_type == PlatformDataType.PLATFORM_DATA_DEPTH.value:
                return PlatformDataTypeIndex.OKEX_FUTURE_DEPTH_DB_INDEX.value


HUOBI_SYMBOL_LIST = ['btcusdt', 'bchusdt', 'ethusdt', 'ltcusdt', 'eosusdt', 'ethbtc', 'eosbtc', 'xrpusdt']
BINANCE_SYMBOL_LIST = ['BTCUSDT', 'BCCUSDT', 'ETHUSDT', 'LTCUSDT', 'EOSUSDT', 'ETHBTC', 'EOSBTC', 'XRPUSDT']
OKEX_SYMBOL_LIST = ['btc_usdt', 'bch_usdt', 'eth_usdt', 'ltc_usdt', 'eos_usdt', 'eth_btc', 'eos_btc', 'xrp_usdt', 'bch_btc', "ltc_btc",  "xrp_btc", "bch_eth",  "ltc_eth", "eos_eth", "xrp_eth"]
OKEX_FUTURE_SYMBOL_LIST = ['btc_usd', 'bch_usd', 'eth_usd', 'ltc_usd', 'eos_usd', None, None, 'xrp_usd']
FCOIN_SYMBOL_LIST = ['btcusdt', 'bchusdt', 'ethusdt', 'ltcusdt', None, None, None, 'xrpusdt']
STANDARD_SYMBOL_LIST = ["BTC/USDT", "BCH/USDT", "ETH/USDT", "LTC/USDT", "EOS/USDT", "ETH/BTC", "EOS/BTC", "XRP/USDT", "BCH/BTC", "LTC/BTC",  "XRP/BTC", "BCH/ETH",  "LTC/ETH", "EOS/ETH", "XRP/ETH"]

@unique
class Coin(Enum):
    """
    币枚举
    """

@unique
class Symbol(Enum):
    """
    货币对枚举
    """
    BTC_USDT = 0
    BCH_USDT = 1
    ETH_USDT = 2
    LTC_USDT = 3
    EOS_USDT = 4
    ETH_BTC = 5
    EOS_BTC = 6
    XRP_USDT = 7
    BCH_BTC = 8
    LTC_BTC = 9
    XRP_BTC = 10
    BCH_ETH = 11
    LTC_ETH = 12
    EOS_ETH = 13
    XRP_ETH = 14

    @staticmethod
    def get_base_symbol(platform):
        list = []
        if (platform.value == Platform.PLATFORM_HUOBI.value):
            pass
        elif (platform.value == Platform.PLATFORM_BINANCE.value):
            pass
        elif (platform.value == Platform.PLATFORM_OKEX.value):
            list.append(Symbol.BTC_USDT)
            list.append(Symbol.ETH_USDT)
        elif (platform.value == Platform.PLATFORM_OKEX_FUTURE.value):
            pass
        elif (platform.value == Platform.PLATFORM_FCOIN.value):
            pass
        return list

    @staticmethod
    def get_currency_pair(platform, symbol):
        """
        获得货币对枚举
        :param platform:平台
        :param symbol:平台货币对
        :return:
        """
        if (platform.value == Platform.PLATFORM_HUOBI.value):
            index = HUOBI_SYMBOL_LIST.index(symbol)
            return Symbol(index)
        elif (platform.value == Platform.PLATFORM_BINANCE.value):
            index = BINANCE_SYMBOL_LIST.index(symbol)
            return Symbol(index)
        elif (platform.value == Platform.PLATFORM_OKEX.value):
            index = OKEX_SYMBOL_LIST.index(symbol)
            return Symbol(index)
        elif (platform.value == Platform.PLATFORM_OKEX_FUTURE.value):
            index = OKEX_FUTURE_SYMBOL_LIST.index(symbol)
            return Symbol(index)
        elif (platform.value == Platform.PLATFORM_FCOIN.value):
            index = FCOIN_SYMBOL_LIST.index(symbol)
            return Symbol(index)

    @staticmethod
    def get_currency_pair_index(platform, symbol):
        """
        获得标准货币对位置索引
        :param platform:平台枚举
        :param symbol:平台货币对
        :return:
        """
        if (platform.value == Platform.PLATFORM_HUOBI.value):
            index = HUOBI_SYMBOL_LIST.index(symbol)
            return index
        elif (platform.value == Platform.PLATFORM_BINANCE.value):
            index = BINANCE_SYMBOL_LIST.index(symbol)
            return index
        elif (platform.value == Platform.PLATFORM_OKEX.value):
            index = OKEX_SYMBOL_LIST.index(symbol)
            return index
        elif (platform.value == Platform.PLATFORM_OKEX_FUTURE.value):
            index = OKEX_FUTURE_SYMBOL_LIST.index(symbol)
            return index
        elif (platform.value == Platform.PLATFORM_FCOIN.value):
            index = FCOIN_SYMBOL_LIST.index(symbol)
            return index

    @staticmethod
    def convert_to_standard_symbol(platform, symbol):
        """
        获得标准货币对
        :param platform:平台枚举
        :param symbol:平台货币对
        :return:
        """
        if (platform.value == Platform.PLATFORM_HUOBI.value):
            index = HUOBI_SYMBOL_LIST.index(symbol)
            return STANDARD_SYMBOL_LIST[index]
        elif (platform.value == Platform.PLATFORM_BINANCE.value):
            index = BINANCE_SYMBOL_LIST.index(symbol)
            return STANDARD_SYMBOL_LIST[index]
        elif (platform.value == Platform.PLATFORM_OKEX.value):
            index = OKEX_SYMBOL_LIST.index(symbol)
            return STANDARD_SYMBOL_LIST[index]
        elif (platform.value == Platform.PLATFORM_OKEX_FUTURE.value and symbol in OKEX_FUTURE_SYMBOL_LIST):
            index = OKEX_FUTURE_SYMBOL_LIST.index(symbol)
            return STANDARD_SYMBOL_LIST[index]
        elif (platform.value == Platform.PLATFORM_FCOIN.value):
            index = FCOIN_SYMBOL_LIST.index(symbol)
            return STANDARD_SYMBOL_LIST[index]
        else:
            return None

    @staticmethod
    def convert_to_platform_symbol(platform, symbol):
        """
        获得平台货币对
        :param platform:平台枚举
        :param symbol:标准货币对
        :return:
        """
        if (platform.value == Platform.PLATFORM_HUOBI.value):
            index = STANDARD_SYMBOL_LIST.index(symbol)
            return HUOBI_SYMBOL_LIST[index]
        elif (platform.value == Platform.PLATFORM_BINANCE.value):
            index = STANDARD_SYMBOL_LIST.index(symbol)
            return BINANCE_SYMBOL_LIST[index]
        elif (platform.value == Platform.PLATFORM_OKEX.value):
            index = STANDARD_SYMBOL_LIST.index(symbol)
            return OKEX_SYMBOL_LIST[index]
        elif (platform.value == Platform.PLATFORM_OKEX_FUTURE.value):
            index = STANDARD_SYMBOL_LIST.index(symbol)
            return OKEX_FUTURE_SYMBOL_LIST[index]
        elif (platform.value == Platform.PLATFORM_FCOIN.value):
            index = STANDARD_SYMBOL_LIST.index(symbol)
            return FCOIN_SYMBOL_LIST[index]

    @staticmethod
    def get_symbol(symbol):
        """
        获得平台货币对
        :param platform:平台枚举
        :param symbol:标准货币对
        :return:
        """
        index = STANDARD_SYMBOL_LIST.index(symbol)
        return Symbol(index)

    @staticmethod
    def get_platform_symbol(platform, currency_pair):
        """
        获得平台货币对
        :param platform:平台枚举
        :param symbol:货币对枚举
        :return:
        """
        if (platform.value == Platform.PLATFORM_HUOBI.value):
            index = currency_pair.value
            return HUOBI_SYMBOL_LIST[index]
        elif (platform.value == Platform.PLATFORM_BINANCE.value):
            index = currency_pair.value
            return BINANCE_SYMBOL_LIST[index]
        elif (platform.value == Platform.PLATFORM_OKEX.value):
            index = currency_pair.value
            return OKEX_SYMBOL_LIST[index]
        elif (platform.value == Platform.PLATFORM_OKEX_FUTURE.value):
            index = currency_pair.value
            return OKEX_FUTURE_SYMBOL_LIST[index]
        elif (platform.value == Platform.PLATFORM_FCOIN.value):
            index = currency_pair.value
            return FCOIN_SYMBOL_LIST[index]

    @staticmethod
    def get_standard_symbol(currency_pair):
        """
        获得标准货币对
        :param platform:平台
        :param symbol:货币对枚举
        :return:
        """
        index = currency_pair.value
        return STANDARD_SYMBOL_LIST[index]


class ContractType(Enum):
    """
    合约类型枚举
    """
    THIS_WEEK = "this_week"
    NEXT_WEEK = "next_week"
    QUARTER = "quarter"


STANDARD_TRADE_TYPE_LIST = ["buy", "sell"]
OKEX_TRADE_TYPE_LIST = ["buy", "sell"]
BINANCE_TRADE_TYPE_LIST = ["BUY", "SELL"]
HUOBI_TRADE_TYPE_LIST = ["buy-limit", "sell-limit"]


class TradeType(Enum):
    """
    交易（下单类型）buy/sell
    """
    BUY = 0
    SELL = 1

    @staticmethod
    def get_trade_type(platform, platform_trade_type):
        """
        获得下单类型枚举
        :param symbol:标准下单类型
        :return:
        """
        if (platform.value == Platform.PLATFORM_HUOBI.value):
            index = HUOBI_TRADE_TYPE_LIST.index(platform_trade_type)
        elif (platform.value == Platform.PLATFORM_BINANCE.value):
            index =  BINANCE_TRADE_TYPE_LIST.index(platform_trade_type)
        elif (platform.value == Platform.PLATFORM_OKEX.value):
            index = OKEX_TRADE_TYPE_LIST.index(platform_trade_type)
        elif (platform.value == Platform.PLATFORM_FCOIN.value):
            # TODO
            pass
        return TradeType(index)

    @staticmethod
    def get_standerd_type(trade_type_enum):
        return STANDARD_TRADE_TYPE_LIST[trade_type_enum.value]

    @staticmethod
    def convert_to_standerd_type(platform, platform_trade_type):
        if (platform.value == Platform.PLATFORM_HUOBI.value):
            index = HUOBI_TRADE_TYPE_LIST.index(platform_trade_type)
        elif (platform.value == Platform.PLATFORM_BINANCE.value):
            index =  BINANCE_TRADE_TYPE_LIST.index(platform_trade_type)
        elif (platform.value == Platform.PLATFORM_OKEX.value):
            index = OKEX_TRADE_TYPE_LIST.index(platform_trade_type)
        elif (platform.value == Platform.PLATFORM_FCOIN.value):
            # TODO
            pass
        return TradeType.get_standerd_type(TradeType(index))

    @staticmethod
    def get_platform_type(platform, trade_type_enum):
        """
        获得平台下单类型
        :param platform:
        :param trade_type:
        :return:
        """
        if (platform.value == Platform.PLATFORM_HUOBI.value):
            index = trade_type_enum.value
            return HUOBI_TRADE_TYPE_LIST[index]
        elif (platform.value == Platform.PLATFORM_BINANCE.value):
            index = trade_type_enum.value
            return BINANCE_TRADE_TYPE_LIST[index]
        elif (platform.value == Platform.PLATFORM_OKEX.value):
            index = trade_type_enum.value
            return OKEX_TRADE_TYPE_LIST[index]
        elif (platform.value == Platform.PLATFORM_FCOIN.value):
            # TODO
            pass


class FutureTradeType(Enum):
    """
    合约交易（下单类型）1:开多 2:开空 3:平多 4:平空
    """
    # 开多
    OPENING_BULL = '1'
    # 开空
    OPENING_BEAR = '2'
    # 平多
    CLOSE_BULL = '3'
    # 平空
    CLOSE_BEAR = '4'


class TransStatus(Enum):
    """
    交易状态
    """
    # 未开始
    NOT_STARTED = "0"
    # 部分完成
    PARTIALLY = "1"
    # 已完成
    COMPLETED = "2"
    # 已撤单
    WITHDRAWAL = "-1"
    # 撤单处理中
    WITHDRAWAL_PROCESSING = "4"

    @staticmethod
    def get_status_by_platform(platform, status):
        _status = str(status)
        # okex futrue订单状态(0等待成交 1部分成交 2全部成交 -1撤单 4撤单处理中 5撤单中)
        if platform == Platform.PLATFORM_OKEX_FUTURE:
            if _status == "5":
                return TransStatus.WITHDRAWAL_PROCESSING.value
            else:
                return _status
        #  okex 订单状态(-1:已撤销  0: 未成交 1: 部分成交 2: 完全成交 3: 撤单处理中)
        elif platform == Platform.PLATFORM_OKEX:
            if _status == "3":
                return TransStatus.WITHDRAWAL_PROCESSING.value
            else:
                return _status
        else:
            return _status


class TransInstStatus(Enum):
    """
    策略实例状态(开仓；开仓已完成；平仓；完成)
    """
    # 开仓
    OPEN_ORDER = "0"
    # 开仓已完成
    OPEN_COMPLET = "1"
    # 平仓
    CLOSE_OUT = "2"
    # 完成
    COMPLET = "3"


class TransType(Enum):
    """
    挂单类型(开仓；平仓；爆仓)
    """
    # 开仓
    OPEN_ORDER = "0"
    # 平仓
    CLOSE_OUT = "1"
    # 爆仓
    OUT_OF_SPACE = "2"


if __name__ == '__main__':
    cp_enum = Symbol.get_currency_pair(Platform.PLATFORM_BINANCE, "BCCUSDT")
    print(cp_enum)
    cp = Symbol.convert_to_standard_symbol(Platform.PLATFORM_BINANCE, "BCCUSDT")
    print(cp)
    symbol = Symbol.get_platform_symbol(Platform.PLATFORM_HUOBI, Symbol.BCH_USDT)
    print(symbol)
    symbol = Symbol.convert_to_platform_symbol(Platform.PLATFORM_OKEX, "EOS/BTC")
    print(symbol)
    st_symbol = Symbol.get_standard_symbol(Symbol.BCH_USDT)
    print(st_symbol)
    print(Symbol.get_symbol("BTC/USDT"))

    print(TradeType.convert_to_standerd_type(Platform.PLATFORM_BINANCE, "SELL"))
    print(TradeType.get_platform_type(Platform.PLATFORM_BINANCE, TradeType.BUY))