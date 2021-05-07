"""
A GLTF 2.0 Generator
"""

from collections import Counter
import copy
import json
import os
import struct

from .accessor import Accessor
from .bufferview import BufferView


class Generator:
    """
    Parameters:
        name, a string that will be used for storing the file and
        set in meshes.
        attribute_order, a list of attributes in the order we parse their vals
    """

    __slots__ = ["__attribute_order", "__json", "__name"]

    # Asset information
    __asset_information = {
        "version": "2.0",
        "generator": "BigWorldDreams",
    }

    # Attribute to Accessor
    __attribute_to_accessor = {
        "POSITION": Accessor(5126, "VEC3", 3),
        "NORMAL": Accessor(5126, "VEC3", 3),
        "TEXTURE": Accessor(5126, "VEC2", 2),
        "COLOR": Accessor(5126, "VEC3", 3),
        "indices": Accessor(5123, "SCALAR", 1),
    }

    def __init__(self, name, attribute_order={"POSITION"}):

        # Set up Variables
        self.__json = {
            "asset": self.__asset_information,
            "scene": 0,
            "scenes": [
                {
                    "nodes": [
                        0
                    ]
                }
            ],
            "nodes": [
                {
                    "mesh": 0
                }
            ],
            "meshes": [
                {
                    "primitives": [
                        {
                            "attributes": {}
                        }
                    ]
                }
            ],
            "accessors": [],
            "bufferViews": [],
            "buffers": [
                {
                    "byteLength": 0,
                    "uri": f"{name}.bin"
                }
            ]
        }
        self.__name = name

        # Valid attribute types
        valid_attributes = self.__attribute_to_accessor.keys()

        # Validate our passed in attribute order.
        for attribute in attribute_order:
            if attribute not in valid_attributes:
                raise ValueError(
                    f"Attribute types must be {valid_attributes}."
                )

        # Set attribute order
        self.__attribute_order = attribute_order

        # Attributes list
        attributes = []
        attributes.append("indices")
        attributes.extend(attribute_order)

        # Build Buffer Views, Accessors, and Meshes
        for attribute in attributes:

            # Accessor
            accessor = copy.copy(self.__attribute_to_accessor[attribute])

            # Buffer Views
            buffer_view = self.__get_buffer_view_by_byte_stride(
                accessor.get_byte_stride()
            )

            # No index with this Stride?
            # Add it!
            if buffer_view is None:
                target = 34963 if attribute == 'indices' else 34962
                buffer_view = BufferView(
                    0, accessor.get_byte_stride(),
                    len(self.__json["bufferViews"]),
                    target
                )
                self.__json["bufferViews"].append(buffer_view)

            # Accessor
            accessor.set_buffer_view(buffer_view)
            self.__json["accessors"].append(accessor)

            # Meshes
            if attribute != "indices":
                self.__json["meshes"][0]["primitives"][0]["attributes"][attribute] = len(self.__json["accessors"]) - 1
            else:
                self.__json["meshes"][0]["primitives"][0]["indices"] = len(self.__json["accessors"]) - 1

    def __str__(self):
        """
        Returns:
            string of the GLTF Json in its current state.
        """
        return f"{self.__json}"

    def add_attribute_sequence(self, attribute_values):
        """
        Adds a sequence of attribute values, based on
        the order of attributes we have.  This is handled
        in a single iteration of the order.

        Parameters:
            attribute_values: a List or Tuple of floats
            that define the GL object.

        For example, if you have POSITION, NORMAL in your order
        this method expects 6 Floats and won't go farther.
        """
        if type(attribute_values) not in (list, tuple):
            raise ValueError('Expected attribute values to be list or tuple.')

        # Starting attribute value
        start = 0

        # Attribute Dict, we build to compare
        # against existing dicts.
        attribute_dict = {}

        # We iterate our attribute order
        for attribute in self.__attribute_order:

            # Attribute's accessor
            attribute_accessor = self.__attribute_to_accessor[attribute]

            # Create an attribute entry
            attribute_dict[attribute] = []

            # Expected attribute values end
            end = start + attribute_accessor.get_element_length()

            # We have enough floats?
            if end > len(attribute_values):
                raise ValueError("Not enough Floats for attributes!")

            # Iterate our range
            for position in range(start, end):
                attribute_value = attribute_values[position]
                attribute_dict[attribute].append(attribute_value)

            # Increment start
            start = end

        # Do we have an indices entry for these values?
        attribute_dict["indices"] = [self.__get_next_index(attribute_dict)]

        # Iterate
        for attribute, values in attribute_dict.items():

            # Set up accessor
            if attribute != 'indices':
                accessor = self.__json["accessors"][
                    self.__json["meshes"][0]["primitives"][0]["attributes"][attribute]
                ]
            else:
                accessor = self.__json["accessors"][
                    self.__json["meshes"][0]["primitives"][0]['indices']
                ]

            # Min/Max/Count
            accessor.add_values(values)

            # Set up buffer view
            buffer_view = accessor.get_buffer_view()

            # If bufferView's byteOffset is None, then we set it
            # to the end of our existing byte total.
            # If both are None, we set our accessor to a byteOffset of 0.
            if buffer_view.get_byte_offset() is None:
                buffer_view.set_byte_offset(self.__get_total_buffer_bytes())
                if accessor.get_byte_offset() is None:
                    accessor.set_byte_offset(0)
            else:
                # We need to look at other bufferViews and update those that
                # use our buffer and are greater than our offset.
                for o_buffer_view in self.__json["bufferViews"]:
                    if(
                        o_buffer_view != buffer_view and
                        o_buffer_view.get_byte_offset() is not None and
                        o_buffer_view.get_buffer() == buffer_view.get_buffer() and
                        o_buffer_view.get_byte_offset() > buffer_view.get_byte_offset()
                    ):
                        o_buffer_view.modify_byte_offset(accessor.get_byte_stride())
                # Accessor doesn't have a byteOffset but the bufferView
                # already has data it references, so set our accessor to the
                # end of the bufferView.
                if accessor.get_byte_offset() is None:
                    accessor.set_byte_offset(buffer_view.get_byte_length())
                # Our accessor has a byteOffset, meaning there could be other
                # accessors using this bufferView.  We need to reach out to
                # them and increment their byteOffset if they already have
                # one and it is greater than ours.
                else:
                    for o_accessor in self.__json["accessors"]:
                        if (
                            o_accessor != accessor and
                            o_accessor.get_byte_offset() is not None and
                            o_accessor.get_buffer_view() == accessor.get_buffer_view() and
                            o_accessor.get_byte_offset() > accessor.get_byte_offset()
                        ):
                            o_accessor.set_byte_offset(accessor.get_byte_length())

            # Set bufferView byteLength
            buffer_view.modify_byte_length(accessor.get_byte_stride())

        # Update our buffer size
        self.__json["buffers"][0]["byteLength"] = self.__get_total_buffer_bytes()

    def __get_accessor_by_bytes(self, desired_bytes):
        """
        Parameters:
            int desired_bytes to find within our Accessors/BufferViews
        Returns:
            Accessor the accessor at the given bytes.

        This requires us to loop through our bufferViews and accessors that
        use those bufferViews.  Since the bufferView knows its byte range
        it is useful for traversing.  The accessor refines that byte range
        with its own offset and applies a componentType which states how
        many bytes each individual item in that range add.  This is imperitive
        since our buffer doesn't care about bytes in its base form.
        """
        for buffer_view in self.__json["bufferViews"]:
            for accessor in self.__json["accessors"]:
                if (
                    buffer_view.get_byte_offset() is not None and
                    accessor.get_byte_offset() is not None and
                    accessor.get_buffer_view() == buffer_view and
                    desired_bytes in range(
                        buffer_view.get_byte_offset() + accessor.get_byte_offset(),
                        buffer_view.get_byte_offset() + accessor.get_byte_offset() + accessor.get_byte_length()
                    )
                ):
                    return accessor
        return None

    def __get_buffer_view_by_byte_stride(self, byte_stride):
        """
        Parameters:
            int a byte_stride
        Returns:
            int of the BufferView that has this stride in it, or -1
            if we can't find one.
        """
        for buffer_view in self.__json["bufferViews"]:
            if buffer_view.get_byte_stride() == byte_stride:
                return buffer_view
        return None

    def __get_next_index(self, attribute_dict):
        """
        Parameters:
            dict attribute/values pair of values being added.
        Returns:
            int of an index if we find the given values already, otherwise
            the length of our existing accessor values length.
        """
        similar_indexes = []
        for attribute, values in attribute_dict.items():
            if attribute in self.__json["meshes"][0]["primitives"][0]["attributes"]:
                accessor = self.__json["accessors"][
                    self.__json["meshes"][0]["primitives"][0]["attributes"][attribute]
                ]
                similar_indexes.extend(accessor.get_similar_value_indexes(values))

        # This gets us an array of one Tuple.  This Tuple is in the format
        # (index, count).  If the count is the same as the number of attributes
        # we have, then we return that index.
        most_common_index = Counter(similar_indexes).most_common(1)
        if len(most_common_index) != 0 and most_common_index[0][1] == len(attribute_dict.keys()):
            return most_common_index[0][0]

        # Returns the length of our latest accessor.
        return accessor.get_count()

    def __get_total_buffer_bytes(self):
        """
        Returns:
            int of bytes across all our BufferViews
        """
        total_bytes = 0
        for buffer_view in self.__json["bufferViews"]:
            total_bytes += buffer_view.get_byte_length()
        return total_bytes

    def save(self, path):
        """
        Parameters:
            string path to where to store our gltf and bin file.
        """

        json_as_string = str(self.__json).replace("'", '"')
        str_as_json = json.loads(json_as_string)
        # dict_as_json = json.loads(str(self.__json))
        print(str_as_json)
        print(json.dumps(str_as_json))
        dict_as_json = json.dumps(json_as_string)
        print(dict_as_json)

        # Grab our Json/GLTF information
        json_info = json.dumps(str(self.__json))
        with open(os.path.join(path, f"{self.__name}.gltf"), "w") as outfile:
            outfile.write(json_info.replace('"', '').replace("'", '"'))

        current_bytes = 0
        pack_data = []
        pack_info = ""
        while current_bytes < self.__get_total_buffer_bytes():
            accessor = self.__get_accessor_by_bytes(current_bytes)
            current_bytes += accessor.get_byte_length()
            pack_data.extend(accessor.get_values_flattened())
            pack_info += accessor.get_struct_type() * accessor.get_total_count()

        # print(pack_data)
        # print(pack_info)

        # Write our binary file
        with open(os.path.join(path, f"{self.__name}.bin"), "wb") as outfile:
            outfile.write(struct.pack(pack_info, *pack_data))
