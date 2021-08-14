"""
    chunk

    A chunk is a x by x mesh.
"""

from .MultiD.src.cube import Cube
from .MultiD.src.cube import Vector3


class Chunk:
    """
    parameters:
        (required)
        [[float, ...]] 2D List of Floats related to the Height.
        (optional)
        float size each block will take up from our Height
        float minimum height, to remove negatives.
        bool should we only include the top most block?
    """

    __slots__ = [
        "__block_size", "__height_data", "__minimum_height", "__size",
        "__top_only", "__triangles",
    ]

    def __init__(
        self,
        height_data, block_size=0.2, minimum_height=0.0, top_only=False
    ):
        self.__block_size = block_size
        self.__height_data = height_data
        self.__minimum_height = minimum_height
        self.__top_only = top_only
        self.__triangles = []

        # Is height_data a 2d array of the same length/width?
        if (
            not isinstance(height_data, list) or
            not isinstance(height_data[0], list) or
            len(height_data) != len(height_data[0])
        ):
            raise ValueError(
                "height_data must be a 2d List of Floats of the same length."
            )

        # Set Chunk Size
        self.__size = len(height_data)

        # Iterate each element in height_data, dividing and creating our
        # tile map
        for y in range(0, self.__size):
            for x in range(0, self.__size):
                if not isinstance(height_data[y][x], float):
                    raise ValueError(
                        "height_data must be a 2d List of Floats."
                    )
                z_max = int(
                    (height_data[y][x] - minimum_height) / self.__block_size
                )
                z_min = -1
                if top_only:
                    z_min = z_max - 1
                for z in range(z_max, z_min, -1):
                    c = Cube(Vector3(float(x), float(z), float(y)))
                    self.__triangles.extend(c.get_triangles())

        # Debug Information
        print(
            f"Created a Chunk of {self.__size}x{self.__size}"
        )

    def clean(self):
        """
        returns:
            int of same number of triangles found
        """
        # return [triangle for triangle in self.__triangles if self.get_triangle_occurrences(triangle) >= 2]
        total_occurrences = 0
        for triangle in self.__triangles:
            occurrences = self.get_triangle_occurrences(triangle)
            if occurrences >= 2:
                total_occurrences += 1
        # return self.__triangles
        return total_occurrences

    def get_triangles(self):
        """
        returns:
            list of Triangles
        """
        return self.__triangles

    def get_triangle_occurrences(self, triangle):
        """
        parameters:
            Triangle to compare against
        returns:
            int of count found that is similar
        """
        occurrences = 0
        for triangle_other in self.__triangles:
            if triangle_other == triangle:
                occurrences += 1
        return occurrences

    def get_vertex_data(self):
        """
        returns:
            [[float, ...]] of vertex data.
        """
        vertex_data = []
        for t in self.__triangles:
            vertex_data.extend(t.get_vertex_data())
        return vertex_data