#!-*-coding:utf-8 -*-
# @TIME    : 2018/7/26/0010 11:56
# @Author  : Luo


class Balance(object):

    def __init__(self, available=0.0, frozen=0.0, balance=0.0):
        """
        :param available: avaiable
        :type available: float
        :param frozen: frozen
        :type frozen: float
        :param balance: balance
        :type balance: float
        :return:
        """
        self._available = available
        self._frozen = frozen
        self._balance = balance

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, value):
        self._available = value

    @property
    def frozen(self):
        return self._frozen

    @frozen.setter
    def frozen(self, value):
        self._frozen = value

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value