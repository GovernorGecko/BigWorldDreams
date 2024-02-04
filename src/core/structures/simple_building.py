"""
simple_building.py
"""


from ...ext.pyGraphics.shape import Shape
from ...ext.pyGraphics.vertex import VertexPositionNormalTexture
from ...ext.pyMultiD.vector import Vector2f, Vector3f

from .compounds.tiled import generate_tiled


def generate_simple_building():
    """
    returns
        Shape

    Might want a Structure component to have as parent.
    """
    # Overall Structure
    shape = Shape(VertexPositionNormalTexture)

    width = 10
    height = 3
    length = 10

    tile_height = 0.2

    # Floor
    floor = generate_tiled(
        width * 0.5,
        length * 0.5,
        tile_height=tile_height,
        texture_minimums=[Vector2f(0.0, 0.0), Vector2f(0.0, 0.5)],
        texture_size=Vector2f(0.5, 0.5),
    )
    floor.cull_vertices()
    floor.center_on_origin()
    # floor.rotate(90.0, 0.0, 0.0)

    shape.add(floor)

    # Wall East
    wall_east = generate_tiled(
        width,
        height,
        tile_height=tile_height,
        ignored_tiles=[[2, 1], [7, 1]],
        texture_minimums=[Vector2f(0.0, 0.0), Vector2f(0.0, 0.5)],
        texture_size=Vector2f(0.5, 0.5),
    )
    wall_east.cull_vertices()
    wall_east.center_on_origin()
    # wall_east.translate(Vector3f(float(width * 0.5), 0.0, 0.0))

    shape.add(wall_east)

    # Return
    return shape
