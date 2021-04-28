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

accessors -> componentType
5120    GL_BYTE
5121    GL_UNSIGNED_BYTE
5122    GL_SHORT
5123    GL_UNSIGNED_SHORT
5124    GL_INT
5125    GL_UNSIGNED_INT
5126    GL_FLOAT
5127    GL_2_BYTES
5128    GL_3_BYTES
5129    GL_4_BYTES

bufferViews -> target (optional)
34962   GL_ARRAY_BUFFER
34963   GL_ELEMENT_ARRAY_BUFFER
"""


class Generator:
    """

    """

    __slots__ = ["__attribute_type_order", "__buffer_views", "__json"]

    # Accessor to GL Type
    __accessor_to_gl_type = {
        "SCALAR": (5123),
        "VEC2": (5126, 5126),
        "VEC3": (5126, 5126, 5126),
    }

    # Asset information
    __asset_information = {
        "version": 2.0,
        "generator": "BigWorldDreams",
    }

    # Attribute to Accessor Type
    __attribute_to_accessor_type = {
        "POSITION": "VEC3",
        "NORMAL": "VEC3",
        "TEXTURE": "VEC2",
        "COLOR": "VEC3",
        "indices": "SCALAR",
    }    

    # GL Type to Byte Count
    __gl_type_to_byte_count = {
        5120: 1,  # GL_BYTE
        5121: 1,  # GL_UNSIGNED_BYTE
        5122: 2,  # GL_SHORT
        5123: 2,  # GL_UNSIGNED_SHORT
        5124: 4,  # GL_INT
        5125: 4,  # GL_UNSIGNED_INT
        5126: 4,  # GL_FLOAT
        5127: 2,  # GL_2_BYTES
        5128: 3,  # GL_3_BYTES
        5129: 4,  # GL_4_BYTES
    }

    def __init__(self, attribute_type_order={"POSITION"}):

        # Set up Variables
        self.__buffer_views = {}
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
                            "attributes": {},
                            "indices": 0
                        }
                    ]
                }
            ],
            "accessors": [],
            "bufferViews": []
        }

        # Valid attribute types
        valid_attribute_types = self.__attribute_to_accessor_type.keys()

        # Validate our passed in attribute order.
        for attribute_type in attribute_type_order:
            if attribute_type not in valid_attribute_types:
                raise ValueError(
                    f"Attribute types must be {valid_attribute_types}."
                )

        # Set attribute order
        self.__attribute_type_order = attribute_type_order

        # Set Meshes
        for attribute_type in self.__attribute_type_order:
            self.__json["meshes"][0]["primitives"][0]["attributes"][attribute_type] = len(self.__json["meshes"][0]["primitives"][0]["attributes"]) + 1

    def __str__(self):
        """
        Returns the GLTF Json in its current state.
        """
        return f"{self.__json}"

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
        for attribute_type in self.__attribute_type_order:

            # Create an attribute_type entry
            attribute_dict[attribute_type] = []

            # How many floats we expecting?
            floats_expected = len(
                self.__get_gl_type_by_attribute(attribute_type)
            )

            # Expected attribute values end
            end = start + floats_expected

            # We have enough floats?
            if end > len(attribute_values):
                raise ValueError("Not enough Floats for attributes!")

            # Iterate our range
            for position in range(start, end):
                attribute_value = attribute_values[position]
                attribute_dict[attribute_type].append(attribute_value)

            # Increment start
            start = end

        print(attribute_dict)

        # This attribute dict not already exist?
        # if attribute_dict not in self.__attributes:
        #    self.__attributes.append(attribute_dict)
        #    self.__indices.append(len(self.__indices))
        # else:
        #    self.__indices.append(self.__attributes.index(attribute_dict))

    def __buffer_data(self, data):
        """
        Given an object of data, handles adding it
        to a buffer view.
        """
        print("hi")

    def __get_bytes_by_attribute(self, attribute):
        """
        Calculate the bytes an attribute takes up.
        """
        b = 0
        for gl_type in self.__get_gl_type_by_attribute(attribute):
            b += self.__gl_type_to_byte_count[gl_type]
        return b

    def __get_gl_type_by_attribute(self, attribute):
        """
        Returns a Tuple, containing the gl type(s)
        that make up the given attribute type.
        """
        return self.__accessor_to_gl_type[
            self.__attribute_to_accessor_type[
                attribute
            ]
        ]

    """
    def build(self):
        Builds and returns our GLTF Json

        # Buffer stores data in a sequence that matches
        # each type of data in line.
        buffer = {}
        for buffer_type in self.__buffer_type_byte_count.keys():
            buffer[buffer_type] = []

        # Unsigned Short
        if len(self.__indices):
            buffer[5123].extend(self.__indices)

        # Floats
        for attribute_type in self.__attribute_type_order:
            for attributes in self.__attributes:
                buffer[5126].extend(attributes[attribute_type])

        # BufferViews mention what type of data is stored in
        # sequence of bytes.
        buffer_views = []

        # GL Element Array Buffer
        if len(self.__indices):
            buffer_views.append(
                {
                    "buffer": 0,
                    "byteOffset": 0,
                    "byteLength": len(self.__indices) * 2,
                    "target": 34963
                })

        # GL Array Buffer

        # Accessors break out Buffer Views to what the data
        # matches in our Mesh
    """
