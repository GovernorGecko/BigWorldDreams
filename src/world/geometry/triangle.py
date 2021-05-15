"""
OpenGL Triangle
"""

from .vector3 import Vector3


class Triangle:
    """
    Parameters:
        [[float, float, float]] x 3 of vertices
    """

    __slots__ = ["__colors", "__normals", "__points", "__texcoords"]

    def __init__(self, *args):
        self.__colors = []
        self.__points = []
        self.__texcoords = []

        if isinstance(args[0], (list, tuple)):
            if len(args[0]) < 3:
                raise ValueError("List or Tuple must be at least 3 values.")
            self.__set(*args[0])
        elif len(args) == 3:
            self.__set(*args)
        else:
            raise ValueError("Didn't receive at least three Vector3s")

        # Calculate Normals
        """
        So for a triangle p1, p2, p3, if the vector U = p2 - p1
        and the vector V = p3 - p1 then the normal N = U X V and
        can be calculated by:
        Nx = UyVz - UzVy
        Ny = UzVx - UxVz
        Nz = UxVy - UyVx
        """
        vector_U = self.__points[1] - self.__points[0]
        vector_V = self.__points[2] - self.__points[0]
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

    def __set(self, point_1, point_2, point_3):
        """
        """
        if not all(isinstance(i, Vector3) for i in [point_1, point_2, point_3]):
            raise ValueError("Didn't receive at least three Vector3s")
        self.__points.append(point_1)
        self.__points.append(point_2)
        self.__points.append(point_3)

    def get_vertex_data(self):
        """
        Parameters:
            [[float, float]] x 3 texture vertices.
        Returns:
            [[float x 8]] x 3 vertexes of this triangle.
        """
        return[
            [*self.__points[0].get_values(), *self.__normals.get_values()],
            [*self.__points[1].get_values(), *self.__normals.get_values()],
            [*self.__points[2].get_values(), *self.__normals.get_values()],
        ]

    def has_vertices(self, vertices):
        """
        """
        if not isinstance(vertices, Vector3):
            return False
        return vertices in self.__points

    def is_like(self, other):
        """
        """
        if not isinstance(other, Triangle):
            return False
        return (
            other.has_vertices(self.__points[0]) and
            other.has_vertices(self.__points[1]) and
            other.has_vertices(self.__points[2])
        )
