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
        stride (how many gl_type per?)
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
        "__buffer_view", "__byte_offset", "__data_type", "__gl_type",
        "__max", "__min", "__values", "__vars_per_value"
    ]

    def __init__(self, gl_type, data_type, vars_per_value):

        # Valid gl type?
        if gl_type not in self.__gl_type_to_byte_count.keys():
            raise ValueError(
                    f"gl_type must be {self.__gl_type_to_byte_count.keys()}."
                )

        self.__gl_type = gl_type
        self.__data_type = data_type
        self.__vars_per_value = vars_per_value

        # Initialize Variables
        self.__buffer_view = None
        self.__byte_offset = None
        self.__max = [0] * vars_per_value
        self.__min = [0] * vars_per_value
        self.__values = []

    def __copy__(self):
        """
        Returns:
            An instance of the Accessor class with the same gl_type,
            data_type, and vars_per_value this instance has.
        """
        return Accessor(
            self.__gl_type, self.__data_type, self.__vars_per_value
        )

    def __repr__(self):
        """
        """
        return self.__str__()
        # return json.dumps(self.get_json())

    def __str__(self):
        """
        """
        return f"{self.get_json()}"

    def add_values(self, values):
        """
        """
        if len(self.__values) == 0:
            self.__max = values
            self.__min = values
        else:
            self.__max = [max(*j) for j in zip(self.__max, values)]
            self.__min = [min(*k) for k in zip(self.__min, values)]
        self.__values.extend(values)

    def get_buffer_view(self):
        """
        """
        return self.__buffer_view

    def get_byte_length(self):
        """
        """
        return self.get_byte_stride() * self.get_count()

    def get_byte_offset(self):
        """
        """
        return self.__byte_offset

    def get_byte_stride(self):
        """
        Returns:
            int of bytes this accessor takes up per set of data
        """
        return self.get_component_type_stride() * self.__vars_per_value

    def get_component_type(self):
        """
        """
        return self.__gl_type

    def get_component_type_stride(self):
        """
        """
        return self.__gl_type_to_byte_count[self.__gl_type]

    def get_count(self):
        """
        """
        return int(len(self.__values) / self.__vars_per_value)

    def get_json(self):
        """
        Returns:
            json accessor object
        """
        return {
            "bufferView": self.__buffer_view,
            "byteOffset": self.__byte_offset,
            "componentType": self.__gl_type,
            "count": self.get_count(),
            "max": self.__max,
            "min": self.__min,
            "type": self.__data_type
        }

    def get_struct_type(self):
        """
        """
        return self.__gl_type_to_struct_type[self.__gl_type]        

    def get_values(self):
        """
        """
        return self.__values

    def get_vars_per_value(self):
        """
        """
        return self.__vars_per_value

    def set_buffer_view(self, buffer_view):
        """
        """
        self.__buffer_view = buffer_view

    def set_byte_offset(self, byte_offset):
        """
        """
        self.__byte_offset = byte_offset
