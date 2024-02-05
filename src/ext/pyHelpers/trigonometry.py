"""
trigonometry.py
"""

import math

from .type_validation import type_validation
from ..pyMultiD.vector import Vector2f, Vector3f


def get_forward_vector3f(phi: float, theta: float, up: str = "z") -> Vector3f:
    """
    parameters
        float
        float
        (optional)
        string
    returns
        Vector3f
    """

    type_validation([phi, theta], float)

    # x = 1.0
    if up == "x":
        return Vector3f(
            math.cos(phi) * math.cos(theta),
            math.cos(phi) * math.sin(theta),
            math.sin(phi),
        )

    # y = 1.0
    elif up == "y":
        return Vector3f(
            math.sin(phi) * math.cos(theta),
            math.cos(phi),
            math.sin(phi) * math.sin(theta),
        )

    # z = 1.0
    else:
        return Vector3f(
            math.cos(phi) * math.sin(theta),
            math.sin(phi),
            math.cos(phi) * math.cos(theta),
        )


def get_vector2f_of_angle(angle: float) -> Vector2f:
    """
    parameters
        float
    returns
        Vector2f
    """

    type_validation(angle, float)

    angle_to_radians = math.radians(angle)

    return Vector2f(math.cos(angle_to_radians), math.sin(angle_to_radians)).normalize()
