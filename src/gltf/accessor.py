"""
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
"""


class Accessor:
    """
    A GLTF2.0 Accessor

    Args:
        gl_type (5126 for GL_FLOAT)
        data_type (SCALAR, VEC3...)
        element_length (how many gl_type per?)
    """

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

    # GL Type to Struct Type
    __gl_type_to_struct_type = {
        5123: "H",
        5126: "f",
    }

    __slots__ = [
        "__buffer_view", "__byte_offset", "__data_type", "__element_length",
        "__gl_type", "__values",
    ]

    def __init__(self, gl_type, data_type, element_length):

        # Valid gl type?
        if gl_type not in self.__gl_type_to_byte_count.keys():
            raise ValueError(
                    f"gl_type must be {self.__gl_type_to_byte_count.keys()}."
                )

        self.__gl_type = gl_type
        self.__data_type = data_type
        self.__element_length = element_length

        # Initialize Variables
        self.__buffer_view = None
        self.__byte_offset = None
        self.__values = []

    def __copy__(self):
        """
        Returns:
            An instance of the Accessor class with the same gl_type,
            data_type, and element_length this instance has.
        """
        return Accessor(
            self.__gl_type, self.__data_type, self.__element_length
        )

    def __repr__(self):
        """
        Returns:
            __str__
        """
        return self.__str__()

    def __str__(self):
        """
        Returns:
            Json representing what gltf requires
        """
        return f"{self.get_json()}"

    def add_values(self, values):
        """
        Parameters:
            List of values to add to our overall list.
        """
        self.__values.append(values)

    def get_buffer_view(self):
        """
        Returns:
            BufferView this Accessor uses.
        """
        return self.__buffer_view

    def get_byte_length(self):
        """
        Returns:
            int that represents the total bytes this Accessor takes up
        """
        return self.get_byte_stride() * self.get_count()

    def get_byte_offset(self):
        """
        Returns:
            int byteOffset of this Accessor from our BufferView
        """
        return self.__byte_offset

    def get_byte_stride(self):
        """
        Returns:
            int of bytes this accessor takes up per set of data
        """
        return self.get_component_type_stride() * self.__element_length

    def get_component_type(self):
        """
        Returns:
            int that is our gl_type
        """
        return self.__gl_type

    def get_component_type_stride(self):
        """
        Returns:
            int representing the bytes our gl_type takes up per element.
        """
        return self.__gl_type_to_byte_count[self.__gl_type]

    def get_count(self):
        """
        Returns:
            int of the number of groups of elements we have.
        """
        return len(self.__values)

    def get_element_length(self):
        """
        Returns:
            int of the element length per group.
        """
        return self.__element_length

    def get_json(self):
        """
        Returns:
            json accessor object
        """
        return {
            "bufferView": self.__buffer_view.get_index(),
            "byteOffset": self.__byte_offset,
            "componentType": self.__gl_type,
            "count": self.get_count(),
            "max": self.get_max_or_min(),
            "min": self.get_max_or_min(min),
            "type": self.__data_type
        }

    def get_max_or_min(self, max_or_min=max):
        """
        Parameters:
            min/max
        Returns:
            min/max group of elements from our values.
        """
        vals = self.__values[0]
        for i in range(1, len(self.__values)):
            vals = [max_or_min(*j) for j in zip(vals, self.__values[i])]
        return vals

    def get_similar_value_indexes(self, search_values):
        """
        Parameters:
            list of values of element length
        Returns:
            list of ints representing indexes where these values were found
        """
        similar_indexes = []
        for i in range(0, len(self.__values)):
            if self.__values[i] == search_values:
                similar_indexes.append(i)
        return similar_indexes

    def get_struct_type(self):
        """
        Returns:
            char of our struct type to pack this gl_type.
        """
        return self.__gl_type_to_struct_type[self.__gl_type]

    def get_total_count(self):
        """
        Returns:
            int of our count multiplied by our elements per value.
        """
        return self.get_count() * self.__element_length

    def get_values(self):
        """
        Returns:
            list of our values, contained in their list of elements.
        """
        return self.__values

    def get_values_flattened(self):
        """
        Returns:
            list of our values, removed from their individual lists.
        """
        return [item for sublist in self.__values for item in sublist]

    def set_buffer_view(self, buffer_view):
        """
        Parameters:
            buffer_view sets our BufferView
        """
        self.__buffer_view = buffer_view

    def set_byte_offset(self, byte_offset):
        """
        Parameters:
            byte_offset sets our byteOffset
        """
        self.__byte_offset = byte_offset
