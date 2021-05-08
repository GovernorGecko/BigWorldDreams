"""
bufferViews -> target (optional)
34962   GL_ARRAY_BUFFER
34963   GL_ELEMENT_ARRAY_BUFFER
"""


class BufferView():
    """
    A GLTF2.0 BufferView

    Parameters:
        int of the buffer this BufferView references
        int offset of this BufferView
        int length of this BufferView
        int stride of this BufferView
        int index of this BufferView in the GLTF Json
        int target for this BufferView
    """

    __slots__ = [
        "__buffer_index", "__byte_offset", "__byte_length",
        "__byte_stride", "__index", "__target"
    ]

    def __init__(self, buffer_index, byte_stride, index, target):
        self.__buffer_index = buffer_index
        self.__byte_stride = byte_stride
        self.__index = index
        self.__target = target

        # Initialize Vars
        self.__byte_offset = None
        self.__byte_length = 0

    def __repr__(self):
        """
        Returns:
            __str__
        """
        return self.__str__()
        # return json.dumps(self.get_json())

    def __str__(self):
        """
        Returns:
            Json representing what gltf requires
        """
        return f"{self.get_json()}"

    def get_buffer(self):
        """
        Returns:
            int our buffer index
        """
        return self.__buffer_index

    def get_byte_length(self):
        """
        Returns:
            int our byte length
        """
        return self.__byte_length

    def get_byte_offset(self):
        """
        Returns:
            int our byte offset
        """
        return self.__byte_offset

    def get_byte_stride(self):
        """
        Returns:
            int our byte stride
        """
        return self.__byte_stride

    def get_index(self):
        """
        Returns:
            int our index in the GLTF Json
        """
        return self.__index

    def get_json(self):
        """
        Returns:
            Json object of our data
        """
        return {
            "buffer": self.__buffer_index,
            "byteOffset": self.__byte_offset,
            "byteLength": self.__byte_length,
            "byteStride": self.__byte_stride,
            "target": self.__target,
        }

    def modify_byte_length(self, value):
        """
        Parameters:
            int to modify our byte length by
        """
        self.__byte_length += value

    def modify_byte_offset(self, value):
        """
        Parameters:
            int to modify our byte offset by
        """
        self.__byte_offset += value

    def set_byte_offset(self, byte_offset):
        """
        Parameters:
            int to set our byte offset to
        """
        self.__byte_offset = byte_offset
