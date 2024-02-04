"""
heightmap

When rendering the sides.  We need to render triangles until the previous z == our z,
then we can render planes.

x = i % width;    // % is the "modulo operator", the remainder of i / width;
y = i / width;    // where "/" is an integer division
"""

import math

from perlin_noise import PerlinNoise

from ...ext.pyGraphics.shape import Shape
from ...ext.pyGraphics.shapes.quadrilateral import generate_quadrilateral
from ...ext.pyGraphics.shapes.triangle import generate_triangle
from ...ext.pyGraphics.vertex import VertexPositionNormalTexture
from ...ext.pyHelpers.type_validation import type_validation
from ...ext.pyMultiD.vector import Vector2f, Vector3f


def generate_heightmap(
    json,
    texture_minimum_side=Vector2f(0.0, 0.0),
    texture_minimum_top=Vector2f(0.0, 0.0),
    texture_size=Vector2f(1.0, 1.0),
):
    """
    parameters
        { name, width, length, heights }
    returns
        Shape
    """

    type_validation(json, object)

    if "heights" not in json or "length" not in json or "width" not in json:
        raise ValueError("JSON file doesn't contain needed fields.")

    heights = json["heights"]
    length = json["length"]
    width = json["width"]

    # Simplification of our Vector3fs we need
    def create_vector3f(x, z):
        return Vector3f((float)(x), (float)(heights[x + length * z]), float(z))

    # Shape
    shape = Shape(VertexPositionNormalTexture)

    # Iterate length/width, creating a Shape
    for z in range(1, length):
        for x in range(1, width):
            shape.add(
                generate_quadrilateral(
                    create_vector3f(x - 1, z - 1),
                    create_vector3f(x, z - 1),
                    create_vector3f(x, z),
                    create_vector3f(x - 1, z),
                    texture_minimum_top,
                    texture_size,
                )
            )

    # X Sides
    for x in range(1, width):
        for z in [0, length - 1]:
            v1 = create_vector3f(x - 1, z)
            v2 = create_vector3f(x, z)
            # We want the larger Y, and then the X from the smaller Y.
            v3 = (
                Vector3f(v1.X, v2.Y, (float)(z))
                if v1.Y > v2.Y
                else Vector3f(v2.X, v1.Y, float(z))
            )

            # If our Y's are equal, no reason to draw a triangle.
            if v1.Y != v2.Y:
                shape.add(
                    generate_triangle(
                        VertexPositionNormalTexture(
                            v3, Vector3f(), texture_minimum_side
                        ),
                        VertexPositionNormalTexture(
                            v2,
                            Vector3f(),
                            Vector2f(
                                texture_minimum_side.X + texture_size.X,
                                texture_minimum_side.Y,
                            ),
                        ),
                        VertexPositionNormalTexture(v1, Vector3f(), texture_size),
                    )
                )

            # Quads Below
            y_list = []

            # V3's Y is the lower number
            y_list.append(v3.Y)

            # If V3's Y isn't 0.0, we'll add its floor to flatten
            # the quads.
            if v3.Y != 0.0:
                y_list.append((float)(math.floor(v3.Y)))

            # Now, we have arbitrary min Y to get to, append until there.
            while y_list[len(y_list) - 1] > -5.0:
                y_list.append(y_list[len(y_list) - 1] - 1.0)

            # Iterate our List, making Quads.
            for i in range(len(y_list) - 1):
                y_min = y_list[i]
                y_max = y_list[i + 1]

                shape.add(
                    generate_quadrilateral(
                        Vector3f(x - 1, y_min, z),
                        Vector3f(x, y_min, z),
                        Vector3f(x, y_max, z),
                        Vector3f(x - 1, y_max, z),
                        texture_minimum_side,
                        texture_size,
                    )
                )

    # Z Sides
    for z in range(1, length):
        for x in [0, width - 1]:
            v1 = create_vector3f(x, z - 1)
            v2 = create_vector3f(x, z)
            # We want the larger Y, and then the Z from the smaller Y.
            v3 = (
                Vector3f((float)(x), v2.Y, v1.Z)
                if v1.Y > v2.Y
                else Vector3f((float)(x), v1.Y, v2.Z)
            )

            # If our Y's are equal, no reason to draw a triangle.
            if v1.Y != v2.Y:
                shape.add(
                    generate_triangle(
                        VertexPositionNormalTexture(
                            v3, Vector3f(), texture_minimum_side
                        ),
                        VertexPositionNormalTexture(
                            v2,
                            Vector3f(),
                            Vector2f(
                                texture_minimum_side.X + texture_size.X,
                                texture_minimum_side.Y,
                            ),
                        ),
                        VertexPositionNormalTexture(v1, Vector3f(), texture_size),
                    )
                )

            # Quads Below
            y_list = []

            # V3's Y is the lower number
            y_list.append(v3.Y)

            # If V3's Y isn't 0.0, we'll add its floor to flatten
            # the quads.
            if v3.Y != 0.0:
                y_list.append((float)(math.floor(v3.Y)))

            # Now, we have arbitrary min Y to get to, append until there.
            while y_list[len(y_list) - 1] > -5.0:
                y_list.append(y_list[len(y_list) - 1] - 1.0)

            # Iterate our List, making Quads.
            for i in range(len(y_list) - 1):
                y_min = y_list[i]
                y_max = y_list[i + 1]

                shape.add(
                    generate_quadrilateral(
                        Vector3f(x, y_min, z - 1),
                        Vector3f(x, y_min, z),
                        Vector3f(x, y_max, z),
                        Vector3f(x, y_max, z - 1),
                        texture_minimum_side,
                        texture_size,
                    )
                )

    # Return Shape
    return shape


def generate_heightmap_json(width, length, octaves=10, seed=1, name="test"):
    """
    parameters
        int
        int
        str
    returns
        json
    """

    type_validation([width, length], int)

    # Generate our Noise
    noise = PerlinNoise(octaves=octaves, seed=seed)

    def get_z(x, y):
        return round(noise([x / width, y / length]), 2)

    return {
        "name": name,
        "width": width,
        "length": length,
        "heights": [get_z(x, y) for y in range(length) for x in range(width)],
    }


def get_slice_from_heightmap(json, z):
    """
    parameters
        { name, width, length, heights }
        int
    """

    if "heights" not in json or "length" not in json or "width" not in json:
        raise ValueError("JSON file doesn't contain needed fields.")

    type_validation(z, int)

    # Store JSON properties
    heights = json["heights"]
    length = json["length"]
    width = json["width"]

    return heights[length * z : width + length * z]
