"""
sphere.py
"""

import math

from ...pyGraphics.shape import Shape
from ...pyGraphics.shapes.triangle import generate_triangle
from ...pyGraphics.vertex import VertexPositionNormalTexture
from ...pyHelpers.type_validation import type_validation
from ...pyMultiD.vector import Vector2f, Vector3f


def generate_sphere(latitudes, longitudes):
    """
    parameters
        int
        int
    return
        Shape
    """
    type_validation([latitudes, longitudes], int)

    delta_latitude = math.pi / latitudes
    delta_longitude = 2 * math.pi / longitudes

    radius = 1.0
    vertices = []

    """
    x = r * cos(phi) * cos(theta)
    y = r * cos(phi) * sin(theta)
    z = r * sin(phi)
    """

    for i in range(latitudes + 1):
        latitude_angle = math.pi / 2 - i * delta_latitude
        # Starting -pi/2 to pi/2
        xy = radius * math.cos(latitude_angle)  # r * cos(phi)
        z = radius * math.sin(latitude_angle)  # r * sin(phi )
        """
        /*
         * We add (latitudes + 1) vertices per longitude because of equator,
         * the North pole and South pole are not counted here, as they overlap.
         * The first and last vertices have same position and normal, but
         * different tex coords.
         */
        """
        for j in range(longitudes + 1):
            longitude_angle = j * delta_longitude

            vertices.append(
                VertexPositionNormalTexture(
                    Vector3f(
                        xy * math.cos(longitude_angle),
                        xy * math.sin(longitude_angle),
                        z,
                    ),
                    Vector3f(),
                    Vector2f(0.0, 0.0),
                )
            )

    # Return Shape
    shape = Shape(VertexPositionNormalTexture)

    """
     *  Indices
     *  k1--k1+1
     *  |  / |
     *  | /  |
     *  k2--k2+1
    """
    for i in range(latitudes):
        k1 = i * (longitudes + 1)
        k2 = k1 + longitudes + 1

        # 2 Triangles per latitude block excluding the first and last longitudes blocks
        for j in range(longitudes):
            if i != 0:
                shape.add(
                    generate_triangle(vertices[k1], vertices[k2], vertices[k1 + 1])
                )

            if i != (latitudes - 1):
                shape.add(
                    generate_triangle(vertices[k1 + 1], vertices[k2], vertices[k2 + 1])
                )

            k1 += 1
            k2 += 1

    # Return Shape
    return shape
