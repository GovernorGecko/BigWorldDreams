"""
chunk

A chunk is a x by x by x mesh.
"""

from .geometry.triangle import Triangle
from .geometry.vector3 import Vector3


class Chunk:
    """
    Parameters:
        [[float, ...]] height_data
        float block_size
        float minimum_height
    """

    __slots__ = [
        "__block_size", "__height_data", "__minimum_height", "__size",
        "__triangles",
    ]

    def __init__(self, height_data, block_size=0.2, minimum_height=0.0):
        self.__block_size = block_size
        self.__height_data = height_data
        self.__minimum_height = minimum_height
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
                for z in range(z_max, -1, -1):
                    self.__add_tile(x, z, y)

        # Debug Information
        print(
            f"Created a Chunk of {self.__size}x{self.__size}x{self.__size}"
        )

    def __add_tile(self, x, y, z):
        """
        Parameters:
            int x position of the tile
            int z position of the tile
            int y position of the tile
        """

        # Top
        self.__triangles.append(
            Triangle([
                Vector3([x + 1, y, z]),
                Vector3([x, y, z]),
                Vector3([x, y, z + 1])
            ])
        )
        self.__triangles.append(
            Triangle([
                Vector3([x, y, z + 1]),
                Vector3([x + 1, y, z + 1]),
                Vector3([x + 1, y, z])
            ])
        )

        """
        # Side X+
        self.__squares.append(
            Square(
                [x + 1, y, z + 1],
                [x + 1, y, z],
                [x + 1, y - 1, z + 1],
                [x + 1, y - 1, z]
            )
        )

        # Side X= (or just X)
        self.__squares.append(
            Square(
                [x, y, z],
                [x, y, z + 1],
                [x, y - 1, z],
                [x, y - 1, z + 1]
            )
        )

        # Side Z+
        self.__squares.append(
            Square(
                [x, y, z + 1],
                [x + 1, y, z + 1],
                [x, y - 1, z + 1],
                [x + 1, y - 1, z + 1]
            )
        )

        # Side Z=
        self.__squares.append(
            Square(
                [x + 1, y, z],
                [x, y, z],
                [x + 1, y - 1, z],
                [x, y - 1, z]
            )
        )

        # Bottom
        self.__squares.append(
            Square(
                [x + 1, y - 1, z],
                [x, y - 1, z],
                [x + 1, y - 1, z + 1],
                [x, y - 1, z + 1]
            )
        )
        """

    def clean(self):
        """
        """
        print("hi")

    def get_vertex_data(self):
        """
        Returns:
            [[float, ...]] of vertex data.
        """
        vertex_data = []
        for t in self.__triangles:
            vertex_data.extend(t.get_vertex_data())
        return vertex_data
