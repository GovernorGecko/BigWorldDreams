"""
vector.py
"""

import math
import operator
from typing import Union

from ..pyHelpers.descriptor import Descriptor
from ..pyHelpers.math import divide_by_zero
from ..pyHelpers.type_validation import type_validation

from .matrix import Matrix


class Vector:
    """
    parameters
        *args
        list<str>
        type

    args are default values for the attributes
    """

    __slots__ = ["__attributes", "__attribute_type", "__dict__"]

    def __init__(self, *args, attributes: list[str], attribute_type: type) -> None:
        if (
            not isinstance(attributes, list)
            or len(attributes) == 0
            or not all(isinstance(a, str) for a in attributes)
        ):
            raise ValueError(
                f"Expected list of Strings for attributes, received {attributes}."
            )

        self.__attributes = attributes
        self.__attribute_type = attribute_type

        # Here we create our Descriptors for the given attributes and set their initial values
        for i in range(len(self.__attributes)):
            attribute = self.__attributes[i]
            value = args[i]

            setattr(self, attribute, Descriptor(self.__attribute_type))
            setattr(self, attribute, value)

    def __repr__(self) -> str:
        """
        returns
            string
        """
        return self.__str__()

    def __str__(self) -> str:
        """
        returns
            string
        """
        return f"{self.get()}"

    def __add__(self, other):
        """
        parameters
            Vector, Float, Int
        returns
            Vector
        """
        return self.__oper(other, operator.add)

    def __eq__(self, other: "Vector") -> bool:
        """
        parameters
            Vector
        returns
            bool
        """
        if not isinstance(other, Vector):
            return False
        return self.get_values_as_list() == other.get_values_as_list()

    def __mul__(self, other: "Vector | float | int") -> "Vector":
        """
        parameters
            Vector, int, float
        returns
            Vector
        """
        return self.__oper(other, operator.mul)

    def __sub__(self, other: "Vector | float | int") -> "Vector":
        """
        parameters
            Vector, int, float
        returns
            Vector
        """
        return self.__oper(other, operator.sub)

    def __truediv__(self, other: "Vector | float | int") -> "Vector":
        """
        parameters
            Vector, int, float
        returns
            Vector
        """
        return self.__oper(other, divide_by_zero)

    def __oper(self, other: "Vector | float | int", operator: operator) -> "Vector":
        """
        parameters
            Vector, int, float
            Python Operator
        returns
            Vector

        We return new instances of our class incase we use += or
        when adding two vectors like v_1 + v_2, we want to return
        a value that is a new vector that doesn't override our
        v_1 or v_2.
        """
        # Int/Float
        if isinstance(other, (int, float)):
            return self.__class__(
                *[operator(j, other) for j in self.get_values_as_list()]
            )
        # Vector
        elif isinstance(other, type(self)):
            return self.__class__(
                *[
                    operator(j, k)
                    for (j, k) in zip(
                        self.get_values_as_list(), other.get_values_as_list()
                    )
                ]
            )
        # Matrix
        # Here we let Matrix handle the operation, then we
        # get those values back and store them in a new classes
        # attributes.
        elif isinstance(other, Matrix):
            return self.__class__(
                *[
                    (other * self.get_values_as_matrix()).get_value(i, 0)
                    for i in range(len(self.__attributes))
                ]
            )

        # Error
        else:
            raise ValueError(f"Expected {type(self)}, int, float, or Matrix")

    def _update(self, other, operator):
        """
        parameters
            Vector, int, float
            Python Operator

        This method works a bit different than the other operations.
        We want to change the values of this instance.  So we must
        call the operation as normal and return a new instance.
        Then we'll use those values to update us.
        """

        # When performing operations, we get new instances of the objects.
        # We want to store the object after the operation and not use it in
        # the below loop, otherwise our values update causing oddities.
        updated_values = self.__oper(other, operator)

        for attribute in self.__attributes:
            setattr(
                self,
                attribute,
                updated_values.get_attribute(attribute),
            )

    def distance(self, other):
        """
        parameters
            Vector
        returns
            float
        """

        type_validation(other, type(self))

        # d = sqrt( pow(x2 - x1) + pow(y2 - y1) +... )
        return math.sqrt(
            sum(
                [
                    math.pow(k - j, 2)
                    for (j, k) in zip(
                        self.get_values_as_list(), other.get_values_as_list()
                    )
                ]
            )
        )

    def dot(self, other):
        """
        parameters
            Vector
        returns
            float
        """

        type_validation(other, type(self))

        return self.__mul__(other).sum()

    def get(self):
        """
        returns
            dict
        """
        return {
            attribute: self.get_attribute(attribute) for attribute in self.__attributes
        }

    def get_attribute(self, attribute):
        """
        parameters
            int/str
        returns
            float/int
        """
        if isinstance(attribute, int):
            return self.get_attribute_by_id(attribute)
        elif isinstance(attribute, str):
            return self.get_attribute_by_name(attribute)
        raise ValueError("Attribute must be int/str.")

    def get_attribute_by_id(self, id):
        """
        parameters
            int
        returns
            float/int
        """
        if not isinstance(id, int) or id < 0 or id >= len(self.__attributes):
            raise ValueError(
                f"Id must be of type int and within range({len(self.__attributes)})."
            )
        return getattr(self, self.__attributes[id])

    def get_attribute_by_name(self, name):
        """ "
        parameters
            str
        returns
            float/int
        """
        if name not in self.__attributes:
            raise ValueError(f"{name} not in {self.__attributes}.")

        return getattr(self, name)

    def get_attributes_as_list(self):
        """
        returns
            list<str>
        """
        return list(self.__attributes)

    def get_values_as_list(self):
        """
        returns
            list<float/int>
        """
        return list(self.get().values())

    def get_values_as_matrix(self):
        """
        returns
            Matrix(Num Properties)x1
        """
        m = Matrix(len(self.__attributes), 1)
        for i in range(len(self.__attributes)):
            m.set_value(i, 0, getattr(self, self.__attributes[i]))
        return m

    def magnitude(self):
        """
        returns
            float
        """
        return math.sqrt(sum([math.pow(x, 2) for x in self.get_values_as_list()]))

    def normalize(self):
        """
        returns
            Vector
        """
        return self.__truediv__(self.magnitude())

    def scale(self, other):
        """
        parameters
            Vector, int, float
        """

        type_validation(other, [type(self), int, float])

        self._update(other, operator.mul)

    def set_attribute(self, attribute, value):
        """
        parameters
            int/str
        """
        if isinstance(attribute, int):
            return self.set_attribute_by_id(attribute, value)
        elif isinstance(attribute, str):
            return self.set_attribute_by_name(attribute, value)
        raise ValueError("Attribute must be int/str.")

    def set_attribute_by_id(self, id, value):
        """
        parameters
            int
        """
        if not isinstance(id, int) or id < 0 or id >= len(self.__attributes):
            raise ValueError(
                f"Id must be of type int and within range({len(self.__attributes)})."
            )
        elif self.__attribute_type != type(value):
            raise ValueError(f"Expected {self.__attribute_type} received {type(value)}")
        setattr(self, self.__attributes[id], value)

    def set_attribute_by_name(self, name, value):
        """ "
        parameters
            str
        """
        if name not in self.__attributes:
            raise ValueError(f"{name} not in {self.__attributes}.")
        elif self.__attribute_type != type(value):
            raise ValueError(f"Expected {self.__attribute_type} received {type(value)}")
        setattr(self, name, value)

    def sum(self):
        """
        returns
            float
        """
        return sum(self.get_values_as_list())

    def translate(self, other):
        """
        parameters
            Vector, int, float
        """

        type_validation(other, (type(self), int, float))

        self._update(other, operator.add)


class Vector2f(Vector):
    """
    parameters
        float
        float
    """

    def __init__(self, x=0.0, y=0.0):
        super().__init__(x, y, attributes=["X", "Y"], attribute_type=float)


class Vector3f(Vector):
    """
    parameters
        float
        float
        float
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__(x, y, z, attributes=["X", "Y", "Z"], attribute_type=float)

    def rotate(self, roll, pitch, yaw):
        """
        parameters
            float/int
            float/int
            float/int

        roll = x
        pitch = y
        yaw = z
        """

        type_validation([roll, pitch, yaw], (float, int))

        # Convert degrees to radians
        pitch_radians = math.radians(pitch)
        roll_radians = math.radians(roll)
        yaw_radians = math.radians(yaw)

        # Pitch, or Y
        pitch_matrix = Matrix(3, 3)

        pitch_matrix.set_value(0, 0, math.cos(pitch_radians))
        pitch_matrix.set_value(2, 0, math.sin(pitch_radians))
        pitch_matrix.set_value(1, 1, 1.0)
        pitch_matrix.set_value(0, 2, -math.sin(pitch_radians))
        pitch_matrix.set_value(2, 2, math.cos(pitch_radians))

        # Roll, or X
        roll_matrix = Matrix(3, 3)

        roll_matrix.set_value(0, 0, 1.0)
        roll_matrix.set_value(1, 1, math.cos(roll_radians))
        roll_matrix.set_value(2, 1, -math.sin(roll_radians))
        roll_matrix.set_value(1, 2, math.sin(roll_radians))
        roll_matrix.set_value(2, 2, math.cos(roll_radians))

        # Yaw, or Z
        yaw_matrix = Matrix(3, 3)

        yaw_matrix.set_value(0, 0, math.cos(yaw_radians))
        yaw_matrix.set_value(1, 0, -math.sin(yaw_radians))
        yaw_matrix.set_value(0, 1, math.sin(yaw_radians))
        yaw_matrix.set_value(1, 1, math.cos(yaw_radians))
        yaw_matrix.set_value(2, 2, 1.0)

        # Order is Yaw * Pitch * Roll
        rotation_matrix = yaw_matrix * pitch_matrix * roll_matrix

        # Update ourself
        self._update(rotation_matrix, operator.mul)
