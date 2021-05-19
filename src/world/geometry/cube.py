"""
Cube
"""

from .triangle import Triangle
from .vector3 import Vector3


class Cube:
    """
        p1----p2
       /|*****/|
      p3----p4*|
      |*p5---|p6
      |/*****|/
      p7----p8
    """

    __slots__ = ["__triangles"]

    def __init__(
        self, center=Vector3(), colors=None, scale=1.0, texcoords=None
    ):
        self.__triangles = []

        # Base center should be a Vector3
        if not isinstance(center, Vector3):
            raise ValueError("Expected a Vector3 for the center.")

        # Scale.
        if not isinstance(scale, float) or scale < 0.0:
            scale = 1.0
        half_scale = scale * 0.5

        # Create our.. points
        p1 = center.offset(x=-half_scale, y=half_scale, z=-half_scale)
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
        self.__triangles.append(Triangle([p6, p5, p7]))
        self.__triangles.append(Triangle([p7, p8, p6]))

    def get_triangles(self):
        """
        """
        return self.__triangles
