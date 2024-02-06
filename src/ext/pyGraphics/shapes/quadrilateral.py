"""
plane.py
"""

from ...pyMultiD.vector import Vector2f, Vector3f
from ...pyHelpers.type_validation import type_validation

from ..vertex import VertexPositionNormalTexture
from ..shape import Shape
from .triangle import generate_triangle


def generate_quadrilateral(
    top_left: Vector3f,
    top_right: Vector3f,
    bottom_right: Vector3f,
    bottom_left: Vector3f,
    texture_minimum: Vector2f = Vector2f(0.0, 0.0),
    texture_size: Vector2f = Vector2f(1.0, 1.0),
):
    """
    parameters
        Vector3f
        Vector3f
        Vector3f
        Vector3f
        Vector2f
        Vector2f

    p1----p2
    |      |
    |      |
    p4----p3
    """

    # Validate Vector3fs
    type_validation([top_left, top_right, bottom_right, bottom_left], Vector3f)

    # Validate Vector2fs
    type_validation([texture_minimum, texture_size], Vector2f)

    # Create Shape
    shape = Shape(VertexPositionNormalTexture)

    shape.add(
        generate_triangle(
            # p2 / Top Right
            VertexPositionNormalTexture(
                top_right,
                Vector3f(),
                texture_minimum + texture_size,
            ),
            # p1 / Top Left
            VertexPositionNormalTexture(
                top_left,
                Vector3f(),
                Vector2f(texture_minimum.X, texture_minimum.Y + texture_size.Y),
            ),
            # p4 / Bottom Left
            VertexPositionNormalTexture(bottom_left, Vector3f(), texture_minimum),
        )
    )
    shape.add(
        generate_triangle(
            # p4 / Bottom Left
            VertexPositionNormalTexture(
                bottom_left,
                Vector3f(),
                texture_minimum,
            ),
            # p3 / Bottom Right
            VertexPositionNormalTexture(
                bottom_right,
                Vector3f(),
                Vector2f(texture_minimum.X + texture_size.X, texture_minimum.Y),
            ),
            # p2 / Top Right
            VertexPositionNormalTexture(
                top_right,
                Vector3f(),
                texture_minimum + texture_size,
            ),
        )
    )

    # Return
    return shape


def generate_quadrilateral_static_axis(
    minimum: Vector2f,
    size: Vector2f,
    axis: str = "x",
    axis_offset: float = 0.0,
    texture_minimum: Vector2f = Vector2f(0.0, 0.0),
    texture_size: Vector2f = Vector2f(1.0, 1.0),
):
    """
    parameters
        Vector2f
        Vector2f
        (optional)
            string
            float
            Vector2f
            Vector2f
    returns
        Shape
    """

    # Y-Axis
    if axis == "y":
        return generate_quadrilateral(
            Vector3f(minimum.X, axis_offset, minimum.Y),
            Vector3f(minimum.X, axis_offset, minimum.Y + size.Y),
            Vector3f(minimum.X + size.X, axis_offset, minimum.Y + size.Y),
            Vector3f(minimum.X + size.X, axis_offset, minimum.Y),
            texture_minimum,
            texture_size,
        )

    # Z-axis
    elif axis == "z":
        return generate_quadrilateral(
            Vector3f(minimum.X, minimum.Y, axis_offset),
            Vector3f(minimum.X, minimum.Y + size.Y, axis_offset),
            Vector3f(minimum.X + size.X, minimum.Y + size.Y, axis_offset),
            Vector3f(minimum.X + size.X, minimum.Y, axis_offset),
            texture_minimum,
            texture_size,
        )

    # X-Axis
    else:
        return generate_quadrilateral(
            Vector3f(axis_offset, minimum.X, minimum.Y),
            Vector3f(axis_offset, minimum.X, minimum.Y + size.Y),
            Vector3f(axis_offset, minimum.X + size.X, minimum.Y + size.Y),
            Vector3f(axis_offset, minimum.X + size.X, minimum.Y),
            texture_minimum,
            texture_size,
        )
