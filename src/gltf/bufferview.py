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
