"""
shape.py
"""

from ..pyHelpers.type_validation import type_validation
from ..pyMultiD.aabb import AABB3f
from ..pyMultiD.vector import Vector, Vector3f

from .vertex import (
    Vertex,
    VertexPosition,
    VertexPositionNormal,
    VertexPositionNormalTexture,
)


class Shape:
    """
    parameters
        Vertex
    """

    __slots__ = ["__aabb", "__indices", "__type", "__vertices"]

    def __init__(self, type: Vertex):
        allowed_types = (
            VertexPosition,
            VertexPositionNormal,
            VertexPositionNormalTexture,
        )

        if type not in allowed_types:
            raise ValueError(f"{type} must be of {allowed_types}")

        self.__aabb = AABB3f()
        self.__indices = []
        self.__type = type
        self.__vertices = [[] for _ in self.get_order()]

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

    def add(self, value: "Shape | Vertex"):
        """
        parameters
            Shape or Vertex
        """

        # Value is a Shape
        if isinstance(value, Shape):
            for i in value.get_indices():
                self.add(self.__type(*value.get_indice_value_by_indice(i)))

        # Value is a Vertex of Type we want (can't use isinstance, that factors in inheritance)
        elif type(value) == self.__type:
            # Return a List of Vectors
            vars = value.get()

            # We have a position?  If so, update our AABB
            if "vp" in self.get_order():
                # Position Index
                vp_index = self.get_order().index("vp")

                # Expand AABB
                self.__aabb.expand(vars[vp_index])

            # Indices of each vertices
            indices = []

            # Iterate, finding indices, or adding new.
            for i in range(len(vars)):
                # Not yet in?
                if vars[i] not in self.__vertices[i]:
                    indices.append(len(self.__vertices[i]))
                    self.__vertices[i].append(vars[i])

                # Already in
                else:
                    indices.append(self.__vertices[i].index(vars[i]))

            # Add indices
            self.__indices.append(indices)

    def center_on_origin(self):
        """
        Uses our AABB Get Center to adjust all
        Positions to origin
        """

        # Do we have the Position element?
        if "vp" not in self.get_order():
            return

        # Index of our Vertex Position
        vp_index = self.get_order().index("vp")

        # Current AABB Center
        aabb_center = self.__aabb.get_center()

        # Iterate Vertices, adjusting positions
        for vp in self.__vertices[vp_index]:
            vp.translate(aabb_center * -1.0)

        # Adjust AABB
        self.__aabb.Maximum -= aabb_center
        self.__aabb.Minimum -= aabb_center

    def cull_vertices(self):
        """
        So.  Culling is in threes.  We are looking for Triangles we already
        have.  If we have two triangles in the same spot, we shouldn't need
        either.

        We iterate Indices, checking positions in threes for other samesies.
        If we find another pair, we need to clear both sets of Indices (including Normals, Textures)

        Check box faces section for orienting triangles
        """

        # For starts, we need a multiple of three indices.
        if not self.is_valid():
            return

        # Secondly, do we have the Position element?
        if "vp" not in self.get_order():
            return

        # Index of our Vertex Position
        vp_index = self.get_order().index("vp")

        # Indices we need to delete
        indices_to_delete = []

        # Iterate Triangles
        for i in range(0, len(self.__indices), 3):
            # Indice Indexes we are looking at
            indice_indexes = [i + j for j in range(3)]

            # Triangle we are using for comparison
            triangle = [
                self.__indices[indice_index][vp_index]
                for indice_index in indice_indexes
            ]

            # Second iteration, we will find ourself.  That is okay.
            for k in range(0, len(self.__indices), 3):
                # Indices to compare against
                indice_indexes_to_compare = [k + j for j in range(3)]

                # Triangle to compare against
                triangle_to_compare = [
                    self.__indices[indice_index][vp_index]
                    for indice_index in indice_indexes_to_compare
                ]

                # We equal!
                if triangle == triangle_to_compare:
                    for indice_index in indice_indexes_to_compare:
                        if indice_index not in indice_indexes:
                            indice_indexes.append(indice_index)

            # Okay.  If we have more than three indexes, that means we found
            # duplicate triangles.
            if len(indice_indexes) > 3:
                for indice_index in indice_indexes:
                    if indice_index not in indices_to_delete:
                        indices_to_delete.append(indice_index)

        # Now, we delete.
        indices_to_delete.sort(reverse=True)
        for indice in indices_to_delete:
            self.delete_indice_at_index(indice)

    def delete_indice_at_index(self, index: int):
        """
        parameters
            int

        Takes in an int in the index, removes it.
        Sees if the indices exists elsewhere, if so, keeps them.
        """

        type_validation(index, int)

        if index < 0 or index >= len(self.__indices):
            return

        # These match up with Vertices
        for i in range(len(self.__indices[index])):
            # Index of the vertice
            vertice_index = self.__indices[index][i]

            # Does this same indice exist in indices at the same spot?
            occurences = 0
            for j in range(len(self.__indices)):
                if vertice_index == self.__indices[j][i]:
                    occurences += 1
                    # We only care if we have more than one occurence
                    if occurences > 1:
                        break

            # Yeap
            if occurences == 1:
                # Delete the Vertice
                del self.__vertices[i][vertice_index]

                # Now we iterate our indices
                for j in range(len(self.__indices)):
                    if self.__indices[j][i] > vertice_index:
                        self.__indices[j][i] -= 1

        # Delete the indice
        del self.__indices[index]

    def get(self) -> list[list[Vector]]:
        """
        returns
            list[list[Vector]]
        """
        return [self.get_indice_value_by_index(i) for i in range(len(self.__indices))]

    def get_aabb(self) -> AABB3f:
        """
        returns
            AABB
        """
        return self.__aabb

    def get_indices(self) -> list[list[int]]:
        """
        returns
            list[List[int]]
        """
        return self.__indices

    def get_indice_value_by_index(self, index: int) -> list[Vector]:
        """
        parameters
            int
        returns
            list[Vector]
        """

        type_validation(index, int)

        if index < len(self.__indices) and index >= 0:
            return self.get_indice_value_by_indice(self.__indices[index])

        return []

    def get_indice_value_by_indice(self, indice: list[int]) -> list[Vector]:
        """
        parameters
            list[int]
        returns
            list[Vector]
        """

        if type(indice) != list or not all(isinstance(i, int) for i in indice):
            raise ValueError("Indice must be a List of Ints.")

        # Indice Length is as expected?
        elif len(indice) != len(self.get_order()):
            raise ValueError(f"Indice Length must be {len(self.get_order())}")

        # Return
        return [
            self.get_vertex_by_indices_index(v, indice[v]) for v in range(len(indice))
        ]

    def get_indices(self) -> list[list[int]]:
        """
        return
            list[list[int]]
        """
        return self.__indices

    def get_order(self) -> list[str]:
        """
        return
            list[str]

            Important for Rotate/Scale/Transition/ObjFile
            CHANGEME
            These should be defined in Vertex, this would allow us to determine return
            order of these values too.  I wanted to use get_attributes but that requires
            the vertex to be initialized, and these are just types...
            Make sure to look for vp/vn/vt to replace as needed
        """
        if self.__type == VertexPosition:
            return ["vp"]
        elif self.__type == VertexPositionNormal:
            return ["vp", "vn"]
        elif self.__type == VertexPositionNormalTexture:
            return ["vp", "vn", "vt"]

        return []

    def get_vertex_by_index(self, v: int) -> list[Vector]:
        """
        parameters
            int
        returns
            list[Vector]
        """

        type_validation(v, int)

        if v >= 0 and v < len(self.__vertices):
            return self.__vertices[v]

        return []

    def get_vertex_by_indices_index(self, v: int, i: int) -> Vector:
        """
        parameters
            int
            int
        returns
            Vector
        """

        # We won't validate v, since we call another method that handles this
        type_validation(i, int)

        if i >= 0 and i < len(self.__vertices[v]):
            return self.get_vertex_by_index(v)[i]

        return []

    def get_vertices(self) -> list[list[Vector]]:
        """
        return
            list[list[Vector]]
        """
        return self.__vertices

    def is_valid(self) -> bool:
        """
        returns
            bool
        """

        return len(self.__indices) > 0 and len(self.__indices) % 3 == 0

    def rotate(self, roll: float, pitch: float, yaw: float) -> "Shape":
        """
        parameters
            float
            float
            float
        returns
            Shape

        Before rotating, be sure to call center_on_origin to so
        everyting rotates around the origin.
        """

        type_validation([roll, pitch, yaw], float)

        # Do we have the Position element?
        if "vp" not in self.get_order():
            return self

        vp_index = self.get_order().index("vp")

        for v in self.__vertices[vp_index]:
            v.rotate(roll, pitch, yaw)

    def scale(self, scale: float) -> "Shape":
        """
        parameters
            float
        returns
            Shape
        """

        type_validation(scale, float)

        # Do we have the Position element?
        if "vp" not in self.get_order():
            return self

        vp_index = self.get_order().index("vp")

        for v in self.__vertices[vp_index]:
            v.scale(scale)

    def translate(self, translation: Vector3f) -> "Shape":
        """
        parameters
            Vector3f
        returns
            Shape
        """

        type_validation(translation, Vector3f)

        # Do we have the Position element?
        if "vp" not in self.get_order():
            return self

        vp_index = self.get_order().index("vp")

        for v in self.__vertices[vp_index]:
            v.translate(translation)
