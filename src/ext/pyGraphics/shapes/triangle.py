"""
triangle.py
"""

from ...pyHelpers.type_validation import type_validation
from ...pyMultiD.vector import Vector3f

from ..shape import Shape
from ..vertex import (
    Vertex,
    VertexPosition,
    VertexPositionNormal,
    VertexPositionNormalTexture,
)


def generate_triangle(vertex1: Vertex, vertex2: Vertex, vertex3: Vertex):
    """
    parameters
        Vertex
        Vertex
        Vertex
    """

    # Vertexes as a List
    vertex_list = [vertex1, vertex2, vertex3]

    # First, are they all Vertex Positions at least?
    type_validation(vertex_list, VertexPosition)

    # We'll take the first Vertex's type, should be all of theirs.
    # We will test below.
    vertex_type = type(vertex_list[0])

    # All Vertexes the same type?
    if not all(type(v) == vertex_type for v in vertex_list[1:]):
        raise ValueError("Triangle Vertexes not of same type.")

    # Only Calculate Normals if needed.
    if vertex_type in [VertexPositionNormal, VertexPositionNormalTexture]:
        """
        So for a triangle p1, p2, p3, if the vector U = p2 - p1
        and the vector V = p3 - p1 then the normal N = U X V and
        can be calculated by:
        Nx = UyVz - UzVy
        Ny = UzVx - UxVz
        Nz = UxVy - UyVx
        """
        position_U = vertex_list[1].Position - vertex_list[0].Position
        position_V = vertex_list[2].Position - vertex_list[0].Position
        normal = Vector3f(
            (position_U.Y * position_V.Z) - (position_U.Z * position_V.Y),
            (position_U.Z * position_V.X) - (position_U.X * position_V.Z),
            (position_U.X * position_V.Y) - (position_U.Y * position_V.X),
        ).normalize()

        # Set all to the Normal
        for v in vertex_list:
            v.Normal = normal

    # Create Shape
    shape = Shape(vertex_type)

    # Add Vertices
    for v in vertex_list:
        shape.add(v)

    # Return
    return shape
