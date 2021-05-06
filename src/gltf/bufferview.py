"""
bufferViews -> target (optional)
34962   GL_ARRAY_BUFFER
34963   GL_ELEMENT_ARRAY_BUFFER
"""


class BufferView():
    """
    """

    __slots__ = [
        "__buffer_index", "__byte_offset", "__byte_length",
        "__byte_stride", "__target"
    ]

    def __init__(self, buffer_index, byte_stride, target):
        self.__buffer_index = buffer_index
        self.__byte_stride = byte_stride
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
        """
        return self.__buffer_index

    def get_byte_length(self):
        """
        """
        return self.__byte_length

    def get_byte_offset(self):
        """
        """
        return self.__byte_offset

    def get_byte_stride(self):
        """
        """
        return self.__byte_stride

    def get_json(self):
        """
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
        """
        self.__byte_length += value

    def modify_byte_offset(self, value):
        """
        """
        self.__byte_offset += value

    def set_byte_offset(self, byte_offset):
        """
        """
        self.__byte_offset = byte_offset
