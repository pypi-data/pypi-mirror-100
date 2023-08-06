"""Serum specific enums."""

from enum import IntEnum


class Side(IntEnum):
    """Side of the orderbook to trade."""

    Buy = 0
    """"""
    Sell = 1
    """"""


class OrderType(IntEnum):
    """"Type of order."""

    Limit = 0
    """"""
    IOC = 1
    """"""
    PostOnly = 2
    """"""


class SelfTradeBehavior(IntEnum):
    DecrementTake = 0
    CancelProvide = 1
    AbortTransaction = 2
