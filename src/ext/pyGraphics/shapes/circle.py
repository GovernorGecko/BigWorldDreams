"""
circle.py
"""

from ...pyGraphics.shape import Shape
from ...pyGraphics.shapes.triangle import generate_triangle
from ...pyGraphics.vertex import VertexPositionNormalTexture
from ...pyHelpers.trigonometry import get_velocity_of_angle
from ...pyHelpers.type_validation import type_validation
from ...pyMultiD.vector import Vector2f, Vector3f


def generate_circle(radius, points):
    """
    parameters
        float
        int
    returns
        Shape
    """

    type_validation([radius, points], [float, int])

    if radius <= 0:
        raise ValueError("Radius must be > 0.")
    elif points < 5:
        raise ValueError("Points must be greater than 4 (otherwise it is a square)")

    # Angle Between each Point / Triangle Wedge
    angle_between_points = 360.0 / points

    # Vector2fs where each point resides in relation to the center
    point_vectors = []

    # Iterate our angles
    # Range can't use Float, so we do it this way.
    current_angle = 0.0
    for _ in range(points):
        # We calculate the Velocity (Vector2f) given the radius/angle
        point_velocity = get_velocity_of_angle(current_angle)
        point_velocity *= radius
        point_vectors.append(point_velocity)
        current_angle += angle_between_points

    # Circle Shape
    shape = Shape(VertexPositionNormalTexture)

    # Generate!
    # We start at the first point, then create a triangle with the following two
    # and so forth.
    for i in range(points - 2):
        shape.add(
            generate_triangle(
                VertexPositionNormalTexture(
                    Vector3f(point_vectors[0].X, point_vectors[0].Y, 0.0),
                    Vector3f(),
                    Vector2f(),
                ),
                VertexPositionNormalTexture(
                    Vector3f(point_vectors[i + 1].X, point_vectors[i + 1].Y, 0.0),
                    Vector3f(),
                    Vector2f(),
                ),
                VertexPositionNormalTexture(
                    Vector3f(point_vectors[i + 2].X, point_vectors[i + 2].Y, 0.0),
                    Vector3f(),
                    Vector2f(),
                ),
            )
        )

    return shape
