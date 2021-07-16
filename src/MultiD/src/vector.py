"""
Vector

This was created for mostly learning.  I wanted to
see how one could create a base Vector class that
Vector2... 3... etc could inherit from.
"""


class Descriptor(object):
    """
    A Descriptor is like @property.setter.  It allows
    us to define a class variable as a getter/setter.

    The one issue is that Descriptors have to be declared
    in the class, not the instance.  So we use an internal
    dictionary for each instance to manage their values.
    """

    def __init__(self):
        self.label = None

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.label, None)

    def __set__(self, instance, value):
        instance.__dict__[self.label] = value


class DescriptorOwner(type):
    """
    Find all descriptors, auto-set their labels.

    By declaring __metaclass__ = DescriptorOwner we
    can easily create and manage all Descriptors in a
    class.
    """

    def __new__(cls, name, bases, attrs):
        for n, v in attrs.items():
            if isinstance(v, Descriptor):
                v.label = n
        return super(DescriptorOwner, cls).__new__(cls, name, bases, attrs)


class Vector():
    """
    Parameters:
        (float, ...) or [float, ...] or float, float
    """

    # Since we don't define Descriptors, this isn't required,
    # but I left it here 'cause... uhm... I really don't know.
    __metaclass__ = DescriptorOwner
    __slots__ = ["__dict__", "__values"]

    def __init__(self, *args, values=[]):

        # Requires a Dict for Values
        if (
            not isinstance(values, list) or
            len(values) == 0 or
            not all(
                isinstance(k, str) for k in values
            )
        ):
            raise ValueError("Values must be a list of length > 0.")
        self.__values = {key: 0.0 for key in values}

        # Error/Type Checking
        if (
            len(args) > 0 and
            isinstance(args[0], (list, tuple))
        ):
            self.set([v for v in args[0]])
        elif(
            len(args) > 0 and
            isinstance(args[0], self.__class__)
        ):
            self.set([v for v in args[0].get_list()])
        elif len(args) == len(self.__values):
            self.set([*args])
        else:
            self.set(None)  # [0.0 for _ in range(len(self.__values))])

        # Dynamic variable creation!
        for v in self.__values.keys():
            setattr(self, v.upper(), Descriptor())
            setattr(self, v.upper(), self.__values[v])

    def __repr__(self):
        """
        Returns:
            __str__()
        """
        return self.__str__()

    def __str__(self):
        """
        Returns:
            str of our values.
        """
        return f"{self.__values}"

    def __eq__(self, other):
        """
        Parameters:
            Vector
        Returns:
            bool if this Vector is equal to another Vector.
        """
        if not isinstance(other, self.__class__):
            return False
        return self.get_list() == other.get_list()

    def __sub__(self, other):
        """
        Parameters:
            Vector
        Returns:
            Vector
        """
        if not isinstance(other, self.__class__):
            raise ValueError(f"Expected {self.__class__}")
        return self.__class__(
            [j - k for (j, k) in zip(
                self.get_list(), other.get_list()
            )])

    def get(self):
        """
        Returns:
            dict of values
        """
        return self.__values

    def get_list(self):
        """
        Returns:
            [float, ...]
        """
        return list(self.__values.values())

    def get_tuple(self):
        """
        Returns:
            (float, ...)
        """
        return tuple(self.__values.values())

    def offset(self, **kwargs):
        """
        Parameters:
            attributes = int/float
        """
        for k, v in kwargs.items():
            if not isinstance(v, (int, float)):
                raise ValueError("Expected Int/Float to offset.")
            elif k in self.__values.keys():
                self.__values[k] += v
        return self

    def set(self, values):
        """
        Parameters:
            [float, ...]
        """
        if (
            not isinstance(values, list) or
            not all(isinstance(v, float) for v in values) or
            not len(values) == len(self.__values)
        ):
            raise ValueError(
                f"Didn't receive at least {len(self.__values)} floats."
            )
        i = 0
        for k in self.__values.keys():
            self.__values[k] = values[i]
            i += 1

    def scale(self, **kwargs):
        """
        Parameters:
            attributes = int/float
        """
        for k, v in kwargs.items():
            if not isinstance(v, (int, float)):
                raise ValueError("Expected Int/Float to scale.")
            elif k in self.__values.keys():
                self.__values[k] *= v
        return self


class Vector2(Vector):
    """
    Vector2
    """

    def __init__(self, *args):
        Vector.__init__(self, *args, values=["x", "y"])


class Vector3(Vector):
    """
    Vector3
    """

    def __init__(self, *args):
        Vector.__init__(self, *args, values=["x", "y", "z"])
