"""
chunk

A chunk is a x by x by x mesh.
"""

from .geometry.square import Square


class Chunk:
    """
    Parameters:
        [[float, ...]] height_data
        float block_size
        float minimum_height
    """

    __slots__ = [
        "__block_size", "__height_data", "__minimum_height", "__size",
        "__squares",
    ]

    def __init__(self, height_data, block_size=0.2, minimum_height=0.0):
        self.__block_size = block_size
        self.__height_data = height_data
        self.__minimum_height = minimum_height
        self.__squares = []

        # Is height_data a 2d array?
        if (
            not isinstance(height_data, list) or
            not isinstance(height_data[0], list)
        ):
            raise ValueError(
                "height_data must be a 2d List of floats."
            )
        # We have the same width/height?
        elif(
            len(height_data) != len(height_data[0])
        ):
            raise ValueError(
                "height_data must be be of equal size for x/y."
            )

        # Set Chunk Size
        self.__size = len(height_data)

        # Iterate each element in height_data, dividing and creating our
        # tile map
        for y in range(0, self.__size):
            for x in range(0, self.__size):
                if not isinstance(height_data[y][x], float):
                    raise ValueError(
                        "height_data must be a 2d List of floats."
                    )
                z_max = int(
                    (height_data[y][x] - minimum_height) / self.__block_size
                )
                for z in range(z_max, -1, -1):
                    self.__add_tile(x, y, z)

        # Debug Information
        print(
            f"Created a Chunk of {self.__size}x{self.__size}x{self.__size}"
        )

    def __add_tile(self, x, z, y):
        """
        Parameters:
            int x positiono of the tile
            int z position of the tile
            int y position of the tile
        """

        # Top
        self.__squares.append(
            Square(
                [x, y, z],
                [x + 1, y, z],
                [x, y, z + 1],
                [x + 1, y, z + 1]
            )
        )

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

    def get_vertex_data(self):
        """
        Returns:
            [[float, ...]] of vertex data.
        """
        vertex_data = []
        for s in self.__squares:
            vertex_data.extend(s.get_vertex_data())
        return vertex_data
