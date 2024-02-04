"""
tiled.py
"""

from ....ext.pyGraphics.shape import Shape
from ....ext.pyGraphics.vertex import VertexPositionNormalTexture
from ....ext.pyHelpers.type_validation import type_validation
from ....ext.pyMultiD.vector import Vector2f, Vector3f

from ..pieces.tile import create_tile


def generate_tiled(
    width=1,
    length=1,
    tile_height=0.2,
    ignored_tiles=[],
    texture_minimums=[Vector2f(0.0, 0.0)] * 2,
    texture_size=Vector2f(1.0, 1.0),
):
    """
    parameters
        (required)
        int
        int
        (optional)
        float
        list<list<int>>
        list<Vector2f>
        Vector2f
    returns
        Shape

    Builds a Shape, setting the Y-Axis to 0.0
    """

    type_validation(
        [width, length, tile_height, ignored_tiles, texture_size],
        [int, int, float, list, Vector2f],
    )

    if not isinstance(texture_minimums, list) or not all(
        type(t) == Vector2f for t in texture_minimums
    ):
        raise ValueError("All Texture Minimums must be Vector2fs")

    shape = Shape(VertexPositionNormalTexture)

    for i in range(width):
        for j in range(length):
            if [i, j] in ignored_tiles:
                continue

            texture_minimum_index = ((i % 2) + (j % 2)) % 2
            texture_minimum = texture_minimums[texture_minimum_index]

            tile = create_tile(
                tile_height,
                texture_minimum=texture_minimum,
                texture_size=texture_size,
            )

            tile.translate(Vector3f(float(i), 0.0, float(j)))

            shape.add(tile)

    return shape
