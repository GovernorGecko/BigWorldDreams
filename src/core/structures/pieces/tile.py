"""
tile.py
"""

from ....ext.pyGraphics.shapes.box import generate_box
from ....ext.pyHelpers.type_validation import type_validation
from ....ext.pyMultiD.vector import Vector2f, Vector3f


def create_tile(
    height=0.2, texture_minimum=Vector2f(0.0, 0.0), texture_size=Vector2f(1.0, 1.0)
):
    """
    returns
        Shape

    Create Tile is meant to create a small box, with a single texture.
    """

    type_validation(height, float)

    if height < 0.0:
        height = 0.1

    return generate_box(
        Vector3f(-0.5, height * -0.5, -0.5),
        Vector3f(0.5, height * 0.5, 0.5),
        texture_minimums=[texture_minimum] * 6,
        texture_size=texture_size,
    )
