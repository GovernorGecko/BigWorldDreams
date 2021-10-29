"""
atlas.py
"""

import os
from PIL import Image


class Atlas():

    __slots__ = [
        "__base_path",
        "__image",
    ]

    def __init__(self, base_path="./", size=1024):

        # Is our base path, valid?
        if not os.path.exists(base_path):
            raise ValueError("Please make sure path exists.")
        # Size must be an int, and a power of 2
        elif (
            not isinstance(size, int) or
            size <= 0
        ):
            raise ValueError(
                "Size must be greater than 0, a power of 2, and an int."
            )

        # Set our base path
        self.__base_path = base_path

        # Create our image
        self.__image = Image.new(mode="RGBA", size=(size, size))

    def add_image(self, filename, path=""):
        """
        """

        # Path to File
        path_to_file = os.path.join(
            self.__base_path, path, filename
        )

        # Exists?
        if not os.path.exists(path_to_file):
            raise ValueError(f"Please make sure {path_to_file} exists.")

        # Image information
        with Image.open(path_to_file) as im:
            print(self.get_open_pixel(im))

    def get_open_pixel(self, image):
        """
        """
        for x in range(self.__image.width):
            for y in range(self.__image.height):
                valid_location = True
                for z in range(image.width):
                    for w in range(image.height):
                        if self.__image.getpixel((x + z, y + w)) != (0, 0, 0, 0):
                            valid_location = False
                            break
                    if not valid_location:
                        break
        return (x, y)


