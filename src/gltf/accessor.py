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

    __slots__ = [
        "__buffer_view", "__byte_offset", "__count", "__data_type",
        "__gl_type", "__max", "__min", "__stride"
    ]

    def __init__(self, gl_type, data_type, stride):
        self.__gl_type = gl_type
        self.__count = 0
        self.__data_type = data_type
        self.__stride = stride

        # Initialize Variables
        self.__buffer_view = None
        self.__byte_offset = None
        self.__count = 0
        self.__max = [0] * stride
        self.__min = [0] * stride

    def __copy__(self):
        """
        """
        return Accessor(self.__gl_type, self.__data_type, self.__stride)

    def __repr__(self):
        """
        """
        return self.__str__()
        # return json.dumps(self.get_json())

    def __str__(self):
        """
        """
        return str(self.get_json())

    def get_buffer_view(self):
        """
        """
        return self.__buffer_view

    def get_byte_offset(self):
        """
        """
        return self.__byte_offset

    def get_byte_stride(self):
        """
        Returns:
            int of bytes this accessor takes up per set of data
        """
        return self.get_component_type_stride() * self.__stride

    def get_component_type(self):
        """
        """
        return self.__gl_type

    def get_component_type_stride(self):
        """
        """
        return self.__gl_type_to_byte_count[self.__gl_type]

    def get_json(self):
        """
        Returns:
            json accessor object
        """
        return {
            "bufferView": self.__buffer_view,
            "byteOffset": self.__byte_offset,
            "componentType": self.__gl_type,
            "count": self.__count,
            "max": self.__max,
            "min": self.__min,
            "type": self.__data_type
        }

    def get_stride(self):
        """
        """
        return self.__stride

    def new_value(self, values):
        """
        """
        self.__count += 1
        self.__max = [max(*j) for j in zip(self.__max, values)]
        self.__min = [min(*k) for k in zip(self.__min, values)]

    def set_buffer_view(self, buffer_view):
        """
        """
        self.__buffer_view = buffer_view

    def set_byte_offset(self, byte_offset):
        """
        """
        self.__byte_offset = byte_offset
