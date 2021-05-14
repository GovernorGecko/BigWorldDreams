"""
OpenGL Triangle
"""

from .vector3 import Vector3


class Triangle:
    """
    Parameters:
        [[float, float, float]] x 3 of vertices
    """

    __slots__ = ["__colors", "__normals", "__texcoords", "__vertices"]

    def __init__(self, vertices, colors=[], textcoords=[]):

        if len(vertices) < 3:
            raise ValueError("Must have at least 3 Vector3s.")
        for v in vertices:
            if not isinstance(v, Vector3):
                raise ValueError("Must pass Vector3.")

        self.__colors = colors
        self.__texcoords = textcoords
        self.__vertices = vertices

        # Calculate Normals
        """
        So for a triangle p1, p2, p3, if the vector U = p2 - p1
        and the vector V = p3 - p1 then the normal N = U X V and
        can be calculated by:
        Nx = UyVz - UzVy
        Ny = UzVx - UxVz
        Nz = UxVy - UyVx
        """
        vector_U = vertices[1] - vertices[0]
        vector_V = vertices[2] - vertices[0]
        self.__normals = Vector3(
            (vector_U.Y * vector_V.Z) - (vector_U.Z * vector_V.Y),
            (vector_U.Z * vector_V.X) - (vector_U.X * vector_V.Z),
            (vector_U.X * vector_V.Y) - (vector_U.Y * vector_V.X),
        )

    def __str__(self):
        """
        Returns:
            string representation of our triangle.
        """
        return str(self.__get_vertex_data())

    def get_vertex_data(self):
        """
        Parameters:
            [[float, float]] x 3 texture vertices.
        Returns:
            [[float x 8]] x 3 vertexes of this triangle.
        """
        return[
            [*self.__vertices[0].get_values(), *self.__normals.get_values()],
            [*self.__vertices[1].get_values(), *self.__normals.get_values()],
            [*self.__vertices[2].get_values(), *self.__normals.get_values()],
        ]
