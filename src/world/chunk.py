"""
chunk

A chunk is a x by x by x mesh.
"""


class Chunk:
    """
    Parameters:
    """

    # Value to divide each noise by to figure out how many blocks (meters)
    # high it is.
    __block_height = 0.2

    __slots__ = [
        "__height", "__height_data", "__minimum_height",
        "__vertex_data", "__width"
    ]

    def __init__(self, height_data, minimum_height=0):
        self.__height_data = height_data
        self.__minimum_height = minimum_height
        self.__vertex_data = []

        # Is height_data a 2d array?
        if (
            not isinstance(height_data, list) or
            not isinstance(height_data[0], list)
        ):
            raise ValueError(
                "height_data must be a 2d List of floats."
            )

        # Set height/width
        self.__height = len(height_data)
        self.__width = len(height_data[0])        

        # Iterate each element in height_data, dividing and creating our
        # tile map
        for y in range(0, self.__height):
            for x in range(0, self.__width):
                if not isinstance(height_data[y][x], float):
                    raise ValueError(
                        "height_data must be a 2d List of floats."
                    )
                z_max = int((height_data[y][x] - minimum_height) / self.__block_height)
                for z in range(z_max, -1, -1):
                    self.__add_tile(x, y, z)

        # print(height_data)
        # print(self.__vertex_data)

    def __add_tile(self, x, y, z):
        """
        """

        # Top
        self.__vertex_data.extend(
            self.__create_square(
                x, y, z
            )
        )

    def __create_square(self, x, y, z, x_mod=1, y_mod=1, z_mod=0):
        """
        """
        vertices = []

        # Triangle 1
        vertices.append([x, z, y])
        vertices.append([x + x_mod, z, y])
        vertices.append([x, z, y + y_mod])

        # Triangle 2
        vertices.append([x + x_mod, z, y])
        vertices.append([x, z, y + y_mod])
        vertices.append([x + x_mod, z, y + y_mod])

        return vertices

    def get_vertex_data(self):
        """
        """
        return self.__vertex_data
