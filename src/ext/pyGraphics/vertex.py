"""
vertex.py
"""

import operator

from ..pyHelpers.descriptor import Descriptor
from ..pyHelpers.type_validation import type_validation

from ..pyMultiD.matrix import Matrix
from ..pyMultiD.vector import Vector2f, Vector3f


class Vertex:
    __slots__ = ["__attributes", "__attribute_types"]

    def __init__(self):
        self.__attributes = []
        self.__attribute_types = []

    def __repr__(self):
        """
        returns
            string
        """
        return self.__str__()

    def __str__(self):
        """
        returns
            string
        """
        return f"{self.get()}"

    def __eq__(self, other):
        """
        parameters
            Vertex
        returns
            bool
        """
        if isinstance(other, Vertex) and type(self) == type(other):
            return all(
                getattr(self, attribute) == getattr(other, attribute)
                for attribute in self.__attributes
            )

        return False

    def _create_attribute(self, attribute, value, attribute_type):
        if not isinstance(attribute, str):
            raise ValueError("Attribute must be a string.")
        elif type(value) != attribute_type:
            raise ValueError(f"Value must be of {attribute_type}")

        self.__attributes.append(attribute)
        self.__attribute_types.append(attribute_type)

        setattr(self, attribute, Descriptor(attribute_type))
        setattr(self, attribute, value)

    def get(self):
        """
        returns
           list(float)
        """
        return [getattr(self, attribute) for attribute in self.__attributes]


class VertexPosition(Vertex):
    """
    parameters
        Vector3f
    """

    def __init__(self, position):
        type_validation(position, Vector3f)

        super().__init__()
        super()._create_attribute("Position", position, Vector3f)

    def __add__(self, other):
        """
        parameters
            Vector3f
        returns
            Vertex
        """
        return self.__oper(other, operator.add)

    def __mul__(self, other):
        """
        parameters
            Matrix
        returns
            Vertex
        """
        return self.__oper(other, operator.mul)

    def __oper(self, other, operation):
        """
        parameters
            any
            operator
        returns
            Vertex
        """

        if isinstance(other, Vertex):
            self.Position = operation(self.Position, other.Position)
        elif isinstance(other, (float, Matrix, Vector3f)):
            self.Position = operation(self.Position, other)

        return self

    def rotate(self, roll=0.0, pitch=0.0, yaw=0.0):
        """
        parameters
            float
            float
            float
        returns
            Vertex
        """

        # Since we are inherited and can have more than Position,
        # and we know Position is slot 0 we do this math.
        # vars = self.get()

        # Position
        # vars[0] = vars[0].rotate(roll, pitch, yaw)

        # Return a new instance of us.
        # return self.__class__(*vars)

        self.Position.rotate(roll, pitch, yaw)

        return self

    def scale(self, scale=1.0):
        """
        parameters
            float
        returns
            Vertex
        """
        return self.__mul__(scale)

    def translate(self, translation):
        """
        parameters
            Vector3f
        returns
            Vertex
        """
        return self.__add__(translation)


class VertexPositionNormal(VertexPosition):
    """
    parameters
        Vector3f
        Vector3f
    """

    def __init__(self, position, normal):
        type_validation(normal, Vector3f)

        super().__init__(position)
        super()._create_attribute("Normal", normal, Vector3f)


class VertexPositionNormalTexture(VertexPositionNormal):
    """
    parameters
        Vector3f
        Vector3f
        Vector2f
    """

    def __init__(self, position, normal, texture):
        type_validation(texture, Vector2f)

        super().__init__(position, normal)
        super()._create_attribute(
            "Texture",
            texture,
            Vector2f,
        )
