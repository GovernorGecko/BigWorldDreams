"""
OpenGL Triangle
This is the base for 3D.  It is made up of three Vertexes that
can contain up to four attributes each.
Position, required, a Vector3
Normal, calculated, a Vector3
TexCoord, optional, a Vector2
Color, optional, a Vector3
"""

from .vector3 import Vector3


class Triangle:
    """
    """

    __slots__ = ["__colors", "__normals", "__positions", "__texcoords"]

    def __init__(self, positions, colors=None, texcoords=None):
        self.__colors = colors
        self.__texcoords = texcoords

        # Expecting three Vector3s
        if (
            isinstance(positions, list) and len(positions) == 3 and
            all(isinstance(p, Vector3) for p in positions)
        ):
            self.__positions = positions
        else:
            raise ValueError("Expecting a List of Vector3s.")

        # Calculate Normals
        """
        So for a triangle p1, p2, p3, if the vector U = p2 - p1
        and the vector V = p3 - p1 then the normal N = U X V and
        can be calculated by:
        Nx = UyVz - UzVy
        Ny = UzVx - UxVz
        Nz = UxVy - UyVx
        """
        position_U = self.__positions[1] - self.__positions[0]
        position_V = self.__positions[2] - self.__positions[0]
        self.__normals = Vector3(
            (position_U.Y * position_V.Z) - (position_U.Z * position_V.Y),
            (position_U.Z * position_V.X) - (position_U.X * position_V.Z),
            (position_U.X * position_V.Y) - (position_U.Y * position_V.X),
        )

    def __repr__(self):
        """
        Returns:
            __str__
        """
        return self.__str__()

    def __str__(self):
        """
        Returns:
            string representation of our triangle.
        """
        return str(self.get_vertex_data())

    def __eq__(self, other):
        """
        Parameters:
            Triangle
        Returns:
            bool of whether both triangles have the same vertexes.
        """
        if not isinstance(other, Triangle):
            return False
        return all(other.has_position(p) for p in self.__positions)

    def get_vertex_data(self):
        """
        Returns:
            [[float x 6]] x 3 vertexes of this triangle.
        """
        return [
            [*p.get_values(), *self.__normals.get_values()]
            for p in self.__positions
        ]

    def has_position(self, position):
        """
        Parameters:
            Vector3
        Returns:
            bool of whether the given Vector3 matches one of ours.
        """
        if not isinstance(position, Vector3):
            return False
        return position in self.__positions
