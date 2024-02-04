"""
atlas.py

Creates a larger image, combined from smaller ones which can then be
used with the json to import textures for renderering objects.

0,0 is the bottom left of the image
"""

import math
import os

from PIL import Image

from ..pyMultiD.vector import Vector2f


class Atlas:
    """
    parameters
        (optional)
        string
            base path to images
        string
            name of the atlas
        int
            size in factor of 2
    """

    __slots__ = [
        "__base_path",
        "__json",
        "__image",
    ]

    def __init__(self, base_path="./", name="atlas", size=1024):
        if not os.path.exists(base_path):
            raise ValueError("Please make sure base path exists.")

        # Size must be an int, and a power of 2
        elif (
            not isinstance(size, int)
            or size <= 0
            or not float(math.log(size, 2)).is_integer()
        ):
            raise ValueError("Size must be greater than 0, a power of 2, and an int.")

        # Used when adding images
        self.__base_path = base_path

        # Create our image
        self.__image = Image.new(mode="RGBA", size=(size, size))

        # JSON that stores location of each added image
        self.__json = {
            "name": name,
            "textures": [],
        }

    def __repr__(self):
        """
        returns
            string
        """
        return self.__str__()

    def __str__(self):
        """
        returns
            string
        """
        return f"{self.get_json()}"

    def add_image(self, filename, name="", sub_path=""):
        """
        parameters
            (required)
            string
                name of the file
            (optional)
            string
                name to give the texture
            string
                sub path to the image in our base path
        returns
            bool
        """

        path_to_file = os.path.join(self.__base_path, sub_path, filename)

        if not os.path.exists(path_to_file):
            raise ValueError(f"Please make sure {path_to_file} exists.")

        # If we didn't pass a name, we use filename as the name
        if name == "":
            name = filename

        with Image.open(path_to_file) as im:
            # This image too large?
            if im.width > self.__image.width or im.height > self.__image.height:
                print(f"Could not add {filename}, doesn't fit base image size.")
                return False

            # Iterate our stored image, looking for our first open pixel.
            for x in range(self.__image.width):
                for y in range(self.__image.height):
                    # Found a spot?
                    spot_found = True

                    # Iterate our texture, looking for a spot.
                    for z in range(im.width):
                        for w in range(im.height):
                            pixel_x = x + w
                            pixel_y = y + z

                            if (
                                pixel_x >= self.__image.width
                                or pixel_y >= self.__image.height
                                or self.__image.getpixel((pixel_x, pixel_y))
                                != (0, 0, 0, 0)
                            ):
                                spot_found = False
                                break
                        else:
                            continue
                        break

                    # Success!
                    if spot_found:
                        # Normalized x/y location of this image
                        normalized_x = x / self.__image.width
                        normalized_y = y / self.__image.height

                        # Normalized size of this image
                        normalized_width = im.width / self.__image.width
                        normalized_height = im.height / self.__image.height

                        # Shaving off
                        # shaved_x = normalized_x / 10
                        # shaved_y = normalized_y / 10

                        # Add image to base image
                        self.__image.paste(im, (x, y))

                        # Add data to json
                        self.__json["textures"].append(
                            {
                                "name": name,
                                "minimumX": normalized_x,
                                "minimumY": 1.0 - normalized_y,
                                "maximumX": normalized_x + normalized_width,
                                "maximumY": (1.0 - normalized_y - normalized_height),
                            }
                        )
                        return True

                else:
                    continue

            # Failure
            print(f"Could not add {filename}, because there was no open spot.")
            return False

    def get_filename(self):
        """
        returns
            string
        """
        return f"{self.__json['name']}.png"

    def get_json(self):
        """
        returns
            JSON
        """
        return self.__json

    def get_texcoords(self, name):
        """
        parameters
            string
                name of the texture
        returns
            list[Vector2f]
        """
        for texture in self.__json["textures"]:
            if texture["name"] == name:
                return [
                    Vector2f(
                        float(texture["minimumX"]),
                        float(texture["minimumY"]),
                    ),
                    Vector2f(
                        float(texture["maximumX"]),
                        float(texture["minimumY"]),
                    ),
                    Vector2f(
                        float(texture["minimumX"]),
                        float(texture["maximumY"]),
                    ),
                    Vector2f(
                        float(texture["maximumX"]),
                        float(texture["maximumY"]),
                    ),
                ]
        return None

    def save(self, path=""):
        """
        parameters
            (optional)
            string
                path to store our atlas
        """

        if not isinstance(path, str):
            raise ValueError("Path must be a string.")

        path_to_store = self.__base_path
        if path != "":
            path_to_store = path

        self.__image.save(os.path.join(path_to_store, self.get_filename()))
