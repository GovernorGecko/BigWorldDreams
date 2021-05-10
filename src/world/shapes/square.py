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

    __slots__ = [
        "__bottom_left", "__bottom_right", "__top_left", "__top_right",
        "__triangles"
    ]

    def __init__(
        self, top_left, top_right, bottom_left, bottom_right
    ):
        self.__top_left = top_left
        self.__top_right = top_right
        self.__bottom_left = bottom_left
        self.__bottom_right = bottom_right

        # Create our Triangles
        self.__triangles = []
        self.__triangles.append(Triangle(
            [top_left, top_right, bottom_left]
        ))
        self.__triangles.append(Triangle(
            [top_right, bottom_left, bottom_right]
        ))

    def __str__(self):
        """
        Returns:
            string vertex data
        """
        return str(self.get_vertex_data())

    def get_vertex_data(self):
        """
        Returns:
            [[float, ...]] of vertex data
        """
        square = []
        for t in self.__triangles:
            square.extend(t.get_vertex_data())
        return square
