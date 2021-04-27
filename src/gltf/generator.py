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

    __slots__ = ["__attributes", "__attribute_order", "__indices", ]

    # Attribute type names and their floats
    __attribute_types = {
        "POSITION": 3,
        "NORMAL": 3,
        "TEXTURE": 2,
        "COLOR": 3
    }

    # Asset information
    __asset_information = {
        "asset": {
            "version": 2.0,
            "generator": "BigWorldDreams",
        }
    }

    # Buffer Type to Byte Count
    __buffer_type_byte_count = {
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

    def __init__(self, attribute_order={"POSITION"}):

        # Set up Variables
        self.__attributes = []
        self.__indices = []

        # Validate our passed in attribute order.
        for attribute_type in attribute_order:
            if attribute_type not in self.__attribute_types.keys():
                raise ValueError(
                    f"Attribute types must be {self.__attribute_types.keys()}."
                )

        # Set attribute order
        self.__attribute_order = attribute_order

    def __str__(self):
        """
        Returns the GLTF Json in its current state.
        """
        return f"{self.build()}"

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
        for attribute_type in self.__attribute_order:

            # Create an attribute_type entry
            attribute_dict[attribute_type] = []

            # How many floats we expecting?
            floats_expected = self.__attribute_types[attribute_type]

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

        # This attribute dict not already exist?
        if attribute_dict not in self.__attributes:
            self.__attributes.append(attribute_dict)
            self.__indices.append(len(self.__indices))
        else:
            self.__indices.append(self.__attributes.index(attribute_dict))

    def build(self):
        """
        Builds and returns our GLTF Json
        """
        json = {
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
            "meshes": [],
            "accessors": [],
            "bufferViews": []
        }

        # Buffer stores data in a sequence that matches
        # each type of data in line.
        buffer = {}
        for buffer_type in self.__buffer_type_byte_count.keys():
            buffer[buffer_type] = []

        # Unsigned Short
        if len(self.__indices):
            buffer[5123].extend(self.__indices)

        # Floats
        for attribute_type in self.__attribute_order:
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

        print(buffer)
        print(buffer_views)

        return json
