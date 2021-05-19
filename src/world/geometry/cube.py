"""
Cube
"""

from .triangle import Triangle
from .vector3 import Vector3


class Cube:
    """
        p1----p2
       /|     /|
      p5|---p6 |
      | p3----p4
      |/     |/
      p7----p8
    """

    __slots__ = ["__triangles"]

    def __init__(self, base_position, colors=None, texcoords=None):
        self.__triangles = []

        # Base Position should be a Vector3
        if not isinstance(base_position, Vector3):
            raise ValueError("Expected a Vector3 for the base_position.")

        # Create our.. points
        p1 = base_position
        p2 = p1.offset(x=1.0)
        p3 = p1.offset(z=1.0)
        p4 = p1.offset(x=1.0, z=1.0)
        p5 = p1.offset(y=-1.0)
        p6 = p5.offset(x=1.0)
        p7 = p5.offset(z=1.0)
        p8 = p5.offset(x=1.0, z=1.0)

        # Top
        self.__triangles.append(Triangle([p2, p1, p3]))
        self.__triangles.append(Triangle([p3, p4, p2]))

        # Side X+
        self.__triangles.append(Triangle([p2, p4, p8]))
        self.__triangles.append(Triangle([p8, p6, p2]))

        # Side X=
        self.__triangles.append(Triangle([p3, p1, p5]))
        self.__triangles.append(Triangle([p5, p7, p3]))

        # Side Z+
        self.__triangles.append(Triangle([p4, p3, p7]))
        self.__triangles.append(Triangle([p7, p8, p4]))

        # Size Z=
        self.__triangles.append(Triangle([p1, p2, p6]))
        self.__triangles.append(Triangle([p6, p5, p1]))

        # Bottom
        self.__triangles.append(Triangle([p8, p7, p5]))
        self.__triangles.append(Triangle([p5, p6, p8]))

    def get_triangles(self):
        """
        """
        return self.__triangles
