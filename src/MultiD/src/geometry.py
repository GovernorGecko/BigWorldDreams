"""
Geometry.py
https://docs.python.org/3/library/dataclasses.html
"""

from dataclasses import dataclass


@dataclass
class Point:
    """
    A 2D Integer Point
    """
    X: int
    Y: int


@dataclass
class Size:
    """
    A 2D Integer Size
    """
    width: int
    height: int
