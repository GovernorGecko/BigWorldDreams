"""
OpenGL Triangle
"""


class Triangle:
    """
    """

    __slots__ = ["__normals", "__vertices"]

    def __init__(self, vertices):
        """
        """
        if (            
            not isinstance(vertices, list) or
            not isinstance(vertices[0], list)
        ):
            raise ValueError(
                "Vertices must be a 2d List of floats."
            )

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
        vector_U = [
            vertices[1][0] - vertices[0][0],
            vertices[1][1] - vertices[0][1],
            vertices[1][2] - vertices[0][2],
        ]
        vector_V = [
            vertices[2][0] - vertices[0][0],
            vertices[2][1] - vertices[0][1],
            vertices[2][2] - vertices[0][2],
        ]
        self.__normals = [
            (vector_U[1] * vector_V[2]) - (vector_U[2] * vector_V[1]),
            (vector_U[2] * vector_V[0]) - (vector_U[0] * vector_V[2]),
            (vector_U[0] * vector_V[1]) - (vector_U[1] * vector_V[0]),
        ]

    def __str__(self):
        """
        """
        return str(self.__normals)

    def get_vertexes(self, texture_vertices=[[0, 0], [1, 0], [1, 1]]):
        """
        """
        return(
            [*self.__vertices[0], *self.__normals, *texture_vertices[0]]
        )
