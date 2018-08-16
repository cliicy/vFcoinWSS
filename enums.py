#  -*- coding:utf-8 -*-
from enum import Enum, unique


@unique
class Platform(Enum):
    """
    交易平台枚举
    """
    PLATFORM_HUOBI = "huobi"
    PLATFORM_BINANCE = "binance"
    PLATFORM_FCOIN = "fcoin"
    PLATFORM_OKEX = "okex"
    PLATFORM_OKEX_FUTURE = "okex_future"


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


HUOBI_SYMBOL_LIST = ['btcusdt', 'bchusdt', 'ethusdt', 'ltcusdt', 'eosusdt', 'ethbtc', 'eosbtc']
BINANCE_SYMBOL_LIST = ['BTCUSDT', 'BCCUSDT', 'ETHUSDT', 'LTCUSDT', 'EOSUSDT', 'ETHBTC', 'EOSBTC']
OKEX_SYMBOL_LIST = ['btc_usdt', 'bch_usdt', 'eth_usdt', 'ltc_usdt', 'eos_usdt', 'eth_btc', 'eos_btc']
OKEX_FUTURE_SYMBOL_LIST = ['btc_usd', 'bch_usd', 'eth_usd', 'ltc_usd', 'eos_usd', None, None]
FCOIN_SYMBOL_LIST = ['btcusdt', 'bchusdt', 'ethusdt', 'ltcusdt', None, None, None]
STANDARD_SYMBOL_LIST = ["BTC/USDT", "BCH/USDT", "ETH/USDT", "LTC/USDT", "EOS/USDT", "ETH/BTC", "EOS/BTC"]


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
        elif (platform.value == Platform.PLATFORM_OKEX_FUTURE.value):
            index = OKEX_FUTURE_SYMBOL_LIST.index(symbol)
            return STANDARD_SYMBOL_LIST[index]
        elif (platform.value == Platform.PLATFORM_FCOIN.value):
            index = FCOIN_SYMBOL_LIST.index(symbol)
            return STANDARD_SYMBOL_LIST[index]

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
            index =currency_pair.value
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

    for enum in FCOIN_SYMBOL_LIST:
        print(enum)
