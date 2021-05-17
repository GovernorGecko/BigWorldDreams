class Vector3():
    """
    Parameters:
        (float, ...) or [float, ...] or float, float, float
    """

    __slots__ = ["__x", "__y", "__z"]

    def __init__(self, *args):
        self.__set(0.0, 0.0, 0.0)

        if isinstance(args[0], (list, tuple)):
            if len(args[0]) < 3:
                raise ValueError("List or Tuple must be at least 3 values.")
            self.__set(*args[0])
        elif len(args) == 3:
            self.__set(*args)
        else:
            raise ValueError("Didn't receive at least three floats/ints.")

    def __repr__(self):
        """
        Returns:
            __str__()
        """
        return self.__str__()

    def __str__(self):
        """
        Returns:
            str of X, Y, Z values.
        """
        return f"{self.X}, {self.Y}, {self.Z}"

    def __eq__(self, other):
        """
        Returns
            bool if this Vector3 is equal to another Vector3.
        """
        if not isinstance(other, Vector3):
            return False
        return (
                other.X == self.X and
                other.Y == self.Y and
                other.Z == self.Z
            )

    def __sub__(self, other):
        """
        Parameters:
            Vector3
        """
        if not isinstance(other, Vector3):
            return None
        return Vector3(
            self.X - other.X,
            self.Y - other.Y,
            self.Z - other.Z
        )

    def __set(self, x, y, z):
        """
        Parameters:
            float, float, float sets our x, y, z.
        """
        self.X = x
        self.Y = y
        self.Z = z

    def get_values(self):
        """
        Returns:
            (float, float, float)
        """
        return [self.X, self.Y, self.Z]

    @property
    def X(self):
        """
        Returns:
            float/int of our x value.
        """
        return self.__x

    @X.setter
    def X(self, value):
        """
        Parameters:
            float/int sets our x value.
        """
        if isinstance(value, (float, int)):
            self.__x = value

    @property
    def Y(self):
        """
        Returns:
            float/int of our y value.
        """
        return self.__y

    @Y.setter
    def Y(self, value):
        """
        Parameters:
            float/int sets our y value.
        """
        if isinstance(value, (float, int)):
            self.__y = value

    @property
    def Z(self):
        """
        Returns:
            float/int of our z value.
        """
        return self.__z

    @Z.setter
    def Z(self, value):
        """
        Parameters:
            float/int sets our z value.
        """
        if isinstance(value, (float, int)):
            self.__z = value