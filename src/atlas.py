"""
atlas.py
"""

import os
from PIL import Image


class Atlas():

    __slots__ = ["__base_path", "__images"]

    def __init__(self, base_path=""):

        if not os.path.exists(base_path):
            raise ValueError("Please make sure path exists.")

        self.__base_path = base_path

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
            print(im.width)

        





