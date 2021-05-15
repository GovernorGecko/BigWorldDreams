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

    def __init__(self, *args):
        self.__colors = []
        self.__vertices = []
        self.__texcoords = []

        if isinstance(args[0], (list, tuple)):
            if len(args[0]) < 3:
                raise ValueError("List or Tuple must be at least 3 values.")
            self.__set(*args[0])
        elif len(args) == 3:
            self.__set(*args)
        else:
            raise ValueError("Didn't receive at least three vertices.")

        # Calculate Normals
        """
        So for a triangle p1, p2, p3, if the vector U = p2 - p1
        and the vector V = p3 - p1 then the normal N = U X V and
        can be calculated by:
        Nx = UyVz - UzVy
        Ny = UzVx - UxVz
        Nz = UxVy - UyVx
        """
        vertex_U = self.__vertices[1] - self.__vertices[0]
        vertex_V = self.__vertices[2] - self.__vertices[0]
        self.__normals = Vector3(
            (vertex_U.Y * vertex_V.Z) - (vertex_U.Z * vertex_V.Y),
            (vertex_U.Z * vertex_V.X) - (vertex_U.X * vertex_V.Z),
            (vertex_U.X * vertex_V.Y) - (vertex_U.Y * vertex_V.X),
        )

    def __str__(self):
        """
        Returns:
            string representation of our triangle.
        """
        return str(self.__get_vertex_data())

    def __set(self, vertex_1, vertex_2, vertex_3):
        """
        Parameters:
            Vector3, Vector3, Vector3
        """
        if not all(
            isinstance(i, Vector3) for i in [vertex_1, vertex_2, vertex_3]
        ):
            raise ValueError("Didn't receive at least three Vector3s")
        self.__vertices.append(vertex_1)
        self.__vertices.append(vertex_2)
        self.__vertices.append(vertex_3)

    def get_vertex_data(self):
        """
        Returns:
            [[float x 6]] x 3 vertexes of this triangle.
        """
        return [
            [
                *v.get_values(), *self.__normals.get_values()
            ] for v in self.__vertices
        ]

    def has_vertex(self, vertex):
        """
        Parameters:
            Vector3
        Returns:
            bool of whether the given Vector3 matches one of ours.
        """
        if not isinstance(vertex, Vector3):
            return False
        return vertex in self.__vertices

    def is_like(self, other):
        """
        Parameters:
            Triangle
        Returns:
            bool of whether both triangles have the same vertexes.
        """
        if not isinstance(other, Triangle):
            return False
        return all(other.has_vertex(v) for v in self.__vertices)
