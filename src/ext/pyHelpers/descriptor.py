"""
descriptor.py
"""

from .type_validation import type_validation


class Descriptor:
    """
    A Descriptor is like @property.setter.  It allows
    us to define a class variable as a getter/setter.
    """

    __slots__ = ["__type", "__value"]

    def __init__(self, type: type = None):
        self.__type = type
        self.__value = None

    def __get__(self, instance, owner):
        return self.__value

    def __set__(self, instance, value):
        if self.__type is not None:
            type_validation([value], self.__type)
        self.__value = value
