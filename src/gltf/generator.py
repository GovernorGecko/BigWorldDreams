"""
A GLTF 2.0 Generator
x	pad byte	        no value
c	char	            bytes of length     1	1
b	signed char	        integer	            1	(1),(3)
B	unsigned char	    integer	            1	(3)
?	_Bool	            bool	            1	(1)
h	short	            integer	            2	(3)
H	unsigned short	    integer	            2	(3)
i	int	                integer	            4	(3)
I	unsigned int	    integer	            4	(3)
l	long	            integer	            4	(3)
L	unsigned long	    integer	            4	(3)
q	long long	        integer	            8	(2), (3)
Q	unsigned long long	integer         	8	(2), (3)
n	ssize_t	            integer	 	            (4)
N	size_t	            integer	 	            (4)
f	float	            float	            4	(5)
d	double	            float	            8	(5)
s	char[]	            bytes
p	char[]	            bytee
P	void *	            integer	 	            (6)
import struct
struct.pack('>f', i)

bufferViews -> target (optional)
34962   GL_ARRAY_BUFFER
34963   GL_ELEMENT_ARRAY_BUFFER
"""

import copy

from .accessor import Accessor


class Generator:
    """
    """

    __slots__ = ["__attribute_order", "__buffer", "__json"]

    # Asset information
    __asset_information = {
        "version": 2.0,
        "generator": "BigWorldDreams",
    }

    # Attribute to Accessor Type
    __attribute_to_accessor_type = {
        "POSITION": Accessor(5126, "VEC3", 3),
        "NORMAL": Accessor(5126, "VEC3", 3),
        "TEXTURE": Accessor(5126, "VEC2", 2),
        "COLOR": Accessor(5126, "VEC3", 3),
        "indices": Accessor(5123, "SCALAR", 3),
    }

    def __init__(self, attribute_order={"POSITION"}):

        # Set up Variables
        self.__buffer = []
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
            "bufferViews": []
        }

        # Valid attribute types
        valid_attributes = self.__attribute_to_accessor_type.keys()

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
            accessor = copy.copy(self.__attribute_to_accessor_type[attribute])

            # Buffer Views
            buffer_view_index = self.__get_buffer_view_by_byte_stride(
                accessor.get_byte_stride()
            )

            # No index with this Stride?
            # Add it!
            if buffer_view_index == -1:
                target = 34964 if attribute == 'indices' else 34962
                self.__json["bufferViews"].append(
                    {
                        "buffer": 0,
                        "byteOffset": None,  # Signifies no data.
                        "byteLength": 0,
                        "byteStride": accessor.get_byte_stride(),
                        "target": target
                    }
                )
                buffer_view_index = len(self.__json["bufferViews"]) - 1

            # Accessor
            accessor.set_buffer_view(buffer_view_index)
            self.__json["accessors"].append(accessor)

            # Meshes
            if attribute != "indices":
                self.__json["meshes"][0]["primitives"][0]["attributes"][attribute] = len(self.__json["accessors"]) - 1
            else:
                self.__json["meshes"][0]["primitives"][0]["indices"] = len(self.__json["accessors"]) - 1

    def __str__(self):
        """
        Returns the GLTF Json in its current state.
        """
        return f"{self.__json} {self.__buffer}"

    def add_attribute_sequence(self, attribute_values):
        """
        Adds a sequence of attribute values, based on
        the order of attributes we have.  This is handled
        in a single iteration of the order.

        Args:
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
            attribute_accessor = self.__attribute_to_accessor_type[attribute]

            # Create an attribute entry
            attribute_dict[attribute] = []

            # Expected attribute values end
            end = start + attribute_accessor.get_stride()

            # We have enough floats?
            if end > len(attribute_values):
                raise ValueError("Not enough Floats for attributes!")

            # Iterate our range
            for position in range(start, end):
                attribute_value = attribute_values[position]
                attribute_dict[attribute].append(attribute_value)

            # Increment start
            start = end

        # Iterate
        for attribute, values in attribute_dict.items():

            # Attribute's accessor
            attribute_accessor = self.__attribute_to_accessor_type[attribute]

            # Set up accessor
            accessor = self.__json["accessors"][
                self.__json["meshes"][0]["primitives"][0]["attributes"][attribute]
            ]

            # Min/Max/Count

            # Set up buffer view
            buffer_view = self.__json["bufferViews"][
                accessor.get_buffer_view()
            ]

            # If bufferView's byteOffset is None, then we set it
            # to the end of our existing byte total.
            # If both are None, we set our accessor to a byteOffset of 0.
            if buffer_view["byteOffset"] is None:
                buffer_view["byteOffset"] = self.__get_total_buffer_bytes()
                if accessor.get_byte_offset() is None:
                    accessor.set_byte_offset(0)
            else:
                # We need to look at other bufferViews and update those that
                # use our buffer and are greater than our offset.
                for o_buffer_view in self.__json["bufferViews"]:
                    if(
                        o_buffer_view != buffer_view and
                        o_buffer_view["byteOffset"] is not None and
                        o_buffer_view["buffer"] == buffer_view["buffer"] and
                        o_buffer_view["byteOffset"] > buffer_view["byteOffset"]
                    ):
                        o_buffer_view["byteOffset"] += accessor.get_byte_stride()
                # Accessor doesn't have a byteOffset but the bufferView
                # already has data it references, so set our accessor to the
                # end of the bufferView.
                if accessor.get_byte_offset() is None:
                    accessor.set_byte_offset(buffer_view["byteLength"])
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
                            o_accessor.set_byte_offset(accessor.get_byte_stride())

            # Insert/Slice into our buffer
            buffer_index = self.__get_buffer_index_by_bytes(
                buffer_view["byteOffset"] + buffer_view["byteLength"]
            )
            self.__buffer[buffer_index:buffer_index] = values

            # Set bufferView byteLength
            buffer_view["byteLength"] += attribute_accessor.get_byte_stride()

    def __get_buffer_index_by_bytes(self, desired_bytes):
        """
        Given a bytes value, finds at what index in our buffer this is at.

        This requires us to loop through our bufferViews and accessors that
        use those bufferViews.  Since the bufferView knows its byte range
        it is useful for traversing.  The accessor refines that byte range
        with its own offset and applies a componentType which states how
        many bytes each individual item in that range add.  This is imperitive
        since our buffer doesn't care about bytes in its base form.
        """
        index = 0
        current_bytes = 0
        while current_bytes < desired_bytes:
            buffer_view_stride = 0
            for buffer_view_index in range(0, len(self.__json["bufferViews"])):
                buffer_view = self.__json["bufferViews"][buffer_view_index]
                for accessor in self.__json["accessors"]:
                    if (
                        buffer_view["byteOffset"] is not None and
                        accessor.get_byte_offset() is not None and
                        accessor.get_buffer_view() == buffer_view_index and
                        current_bytes >= buffer_view["byteOffset"] + accessor.get_byte_offset() and
                        current_bytes < buffer_view["byteOffset"] + buffer_view["byteLength"]
                    ):
                        buffer_view_stride = accessor.get_component_type_stride()
                        break
                if buffer_view_stride != 0:
                    current_bytes += buffer_view_stride
                    index += 1
                    break
        return index

    def __get_buffer_view_by_byte_stride(self, byte_stride):
        """
        Given a byte stride, finds which Buffer View it belongs
        to, if it already exists.
        """
        for i in range(0, len(self.__json["bufferViews"])):
            if self.__json["bufferViews"][i]["byteStride"] == byte_stride:
                return i
        return -1

    def __get_total_buffer_bytes(self):
        """
        Gets our total bytes in our buffer
        """
        total_bytes = 0
        for buffer_view in self.__json["bufferViews"]:
            total_bytes += buffer_view["byteLength"]
        return total_bytes
