"""
OpenGL Square
"""

from .triangle import Triangle


class Square:
    """
    Parameters:
        [float, float, float]
            top_left
            top_right
            bottom_left
            bottom_right
    """

    __slots__ = ["__triangles"]

    def __init__(
        self, top_left, top_right, bottom_left, bottom_right
    ):
        # Create our Triangles
        # Using CCW
        self.__triangles = []
        self.__triangles.append(Triangle(
            [top_right, top_left, bottom_left]
        ))
        self.__triangles.append(Triangle(
            [bottom_left, bottom_right, top_right]
        ))

    def __str__(self):
        """
        Returns:
            string vertex data
        """
        return str(self.get_vertex_data())

    def get_triangles(self):
        """
        Returns:
            list[Triangle]
        """
        return self.__triangles

    def get_vertex_data(self):
        """
        Returns:
            [[float, ...]] of vertex data
        """
        square = []
        for triangle in self.__triangles:
            square.extend(triangle.get_vertex_data())
        return square
