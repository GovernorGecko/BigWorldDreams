"""
aabb
"""

from ..pyHelpers.descriptor import Descriptor

from .vector import Vector3f


class AABB:
    """
    parameters
        Vector
        Vector
        (optional)
        Type
    """

    __slots__ = ["__dict__", "__type"]

    def __init__(self, minimum, maximum, aabb_type):
        if not isinstance(aabb_type, type):
            raise ValueError("Expected a Type.")

        self.__type = aabb_type

        # Maximum
        setattr(self, "Maximum", Descriptor(self.__type))
        setattr(self, "Maximum", maximum)

        # Minimum
        setattr(self, "Minimum", Descriptor(self.__type))
        setattr(self, "Minimum", minimum)

    def __repr__(self):
        """
        returns
            str
        """
        return self.__str__()

    def __str__(self):
        """
        returns
            str
        """
        return f"{self.Minimum} {self.Maximum}"

    def expand(self, vector):
        """
        parameters
            vector
        """

        if not self.__type == type(vector):
            raise ValueError(f"AABB is of type {self.__type}, received {type(vector)}.")

        for attribute in vector.get_attributes_as_list():
            if vector.get_attribute(attribute) < self.Minimum.get_attribute(attribute):
                self.Minimum.set_attribute(attribute, vector.get_attribute(attribute))
            elif vector.get_attribute(attribute) > self.Maximum.get_attribute(
                attribute
            ):
                self.Maximum.set_attribute(attribute, vector.get_attribute(attribute))

    def get_center(self):
        """
        returns
            Vector
        """

        return self.Minimum + ((self.Maximum - self.Minimum) * 0.5)

    def is_colliding_with_aabb(self, aabb):
        """
        parameters
            AABB
        returns
            bool
        """

        if not self.__type == type(aabb):
            raise ValueError(f"AABB is of type {self.__type}, received {type(aabb)}.")

        # Equivalent to (this.Maximum.X < aabb.Minimum.X) || (this.Minimum.X > aabb.Maximum.X)
        # For each attribute (x, y, z...)
        for attribute in self.Maximum.get_attributes_as_list():
            if (
                self.Maximum.get_attribute(attribute)
                < aabb.Minimum.get_attribute(attribute)
            ) or (
                self.Minimum.get_attribute(attribute)
                > aabb.Maximum.get_attribute(attribute)
            ):
                return False
        return True

    def is_colliding_with_point(self, point):
        """
        parameters
            Vector
        returns
            bool
        """

        if self.__type != type(point):
            raise ValueError(f"AABB is of type {self.__type}, received {type(point)}.")

        # Same as point.X >= this.Minimum.X && point.X <= this.Maximum.X
        # For each attribute (x, y, z...)
        return all(
            (point.get_attribute(attribute) >= self.Minimum.get_attribute(attribute))
            and (
                point.get_attribute(attribute) <= self.Maximum.get_attribute(attribute)
            )
            for attribute in self.Maximum.get_attributes_as_list()
        )


class AABB3f(AABB):
    """
    parameters
        Vector3f
        Vector3f
    """

    def __init__(self, minimum=Vector3f(), maximum=Vector3f()):
        super().__init__(minimum, maximum, Vector3f)
