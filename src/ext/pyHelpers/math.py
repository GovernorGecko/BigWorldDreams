"""
math.py
"""

import operator

from .type_validation import type_validation


def divide_by_zero(a: int | float, b: int | float) -> int | float:
    """
    parameters
        int/float
        int/float
    returns
        int/float
    """

    type_validation([a, b], (float, int))

    if b == 0:
        return 0.0
    else:
        return operator.truediv(a, b)


def dot_of_lists(
    list_one: list[int | float], list_two: list[int | float]
) -> list[int | float]:
    """
    parameters
        list[int/float]
        list[int/float]
    returns
        list[int/float]
    """

    type_validation([list_one, list_two], list)

    if len(list_one) != len(list_two):
        return 0
    elif not all(isinstance(a, (int, float)) for a in zip(list_one, list_two)):
        raise ValueError("All elements of each list must be ints/floats")

    return sum(i[0] * i[1] for i in zip(list_one, list_two))


def get_max_and_min_from_list(
    a_list: list[int | float],
) -> "tuple(int | float, int | float)":
    """
    parameters
        list[int/float]
    returns
        tuple(int/float, int/float)
    """

    if not isinstance(a_list, list) or not all(
        isinstance(a, (float, int)) for a in a_list
    ):
        raise ValueError("Expected a list of ints and/or floats")

    return (min(a_list), max(a_list))
