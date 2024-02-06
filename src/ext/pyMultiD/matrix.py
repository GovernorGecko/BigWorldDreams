"""
matrix.py
"""

from ..pyHelpers.math import dot_of_lists


class Matrix:
    """
    parameters
        (optional)
            int
            int
    """

    __slots__ = ["__matrix"]

    def __init__(self, rows: int = 1, columns: int = 1):
        if (
            not isinstance(columns, int)
            or not isinstance(rows, int)
            or columns <= 0
            or rows <= 0
        ):
            ValueError("Columns and Rows must be ints > 0")

        self.__matrix = [[0.0 for _ in range(columns)] for _ in range(rows)]

    def __str__(self) -> str:
        """
        returns
            string
        """
        return str(self.__matrix)

    def __mul__(self, other: "Matrix") -> "Matrix":
        """
        parameters
            Matrix
        returns
            Matrix
        """

        if not isinstance(other, Matrix):
            ValueError(f"{type(other)} is not Matrix")
        elif self.get_columns_length() != other.get_rows_length():
            ValueError("Expected our columns to equal other's rows.")

        # Create a new matrix, using our column length
        new_matrix = Matrix(
            self.get_rows_length(),
            other.get_columns_length(),
        )

        # Our Rows to Columns, multiplied by other Columns to Rows
        for i in range(self.get_rows_length()):
            for j in range(other.get_columns_length()):
                new_matrix.set_value(
                    i,
                    j,
                    dot_of_lists(
                        self.__matrix[i],
                        other.get_column_values(j),
                    ),
                )

        return new_matrix

    def get_columns_length(self) -> int:
        """
        returns
            int
        """
        return len(self.__matrix[0])

    def get_column_values(self, column: int) -> list[float | int]:
        """
        parameters
            int
        returns
            list[float/int]
        """
        if not self.is_valid_column(column):
            ValueError(f"{column} not valid for Matrix")
        return [row[column] for row in self.__matrix]

    def get_rows_length(self) -> int:
        """
        returns
            int
        """
        return len(self.__matrix)

    def get_value(self, row: int, column: int) -> float | int:
        """
        parameters
            int
            int
        returns
            float/int
        """
        if not self.is_valid_column(column) or not self.is_valid_row(row):
            ValueError(f"{column} or {row} not valid for Matrix")
        return self.__matrix[row][column]

    def get_values_as_list(self) -> float | int:
        """
        returns
            list[float/int]
        """
        return [j for sub in self.__matrix for j in sub]

    def is_valid_column(self, column: int) -> bool:
        """
        parameters
            int
        returns
            bool
        """
        if (
            not isinstance(column, int)
            or column < 0
            or self.get_columns_length() <= column
        ):
            return False
        return True

    def is_valid_row(self, row: int) -> bool:
        """
        parameters
            int
        returns
            bool
        """
        if not isinstance(row, int) or row < 0 or self.get_rows_length() <= row:
            return False
        return True

    def set_value(self, row: int, column: int, value: float | int):
        """
        parameters
            int
            int
            float/int
        """
        if not self.is_valid_column(column) or not self.is_valid_row(row):
            ValueError(f"{column} or {row} not valid for Matrix")
        elif not isinstance(value, (float, int)):
            ValueError("Value must be a float or int.")
        self.__matrix[row][column] = value
