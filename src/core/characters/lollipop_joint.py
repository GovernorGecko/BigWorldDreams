"""
lollipop_joint

3D Code
---
pitch_radians = math.radians(self.__pitch)
yaw_radians = math.radians(self.__yaw)
get_forward_vector(pitch_radians, yaw_radians, up="x")
"""

from ...ext.pyGraphics.shape import Shape
from ...ext.pyGraphics.shapes.circle import generate_circle
from ...ext.pyGraphics.shapes.quadrilateral import generate_quadrilateral
from ...ext.pyGraphics.vertex import VertexPositionNormalTexture
from ...ext.pyHelpers.trigonometry import get_vector2f_of_angle
from ...ext.pyHelpers.type_validation import type_validation
from ...ext.pyMultiD.vector import Vector2f, Vector3f


class LollipopJoint:
    """
    parameters
        float
        float
        float
        float
    """

    __slots__ = [
        "__children",
        "__length",
        "__parent",
        "__rotation",
        "__width",
        "__z_offset",
    ]

    def __init__(
        self,
        length: float,
        width: float = 0.0,
        rotation: float = 0.0,
        z_offset: float = 0.0,
    ):
        type_validation([length, width], float)

        self.__children = []
        self.__length = length
        self.__parent = None
        self.set_rotation(rotation)
        self.__width = width
        self.set_z_offset(z_offset)

    def add(self, joint: "LollipopJoint") -> None:
        """
        parameters
            LollipopJoint
        """
        type_validation(joint, LollipopJoint)

        # Does this joint already have a parent?
        if joint.get_parent() is not None:
            raise ValueError("joint already has a parent, can't make a child.")
        # Is this joint, us?
        elif joint == self:
            raise ValueError("joint is us.")
        # Is this joint already in our linked list?
        elif self.get_root().is_joint_in_children(joint):
            raise ValueError("joint is already in joint tree.")

        # Set Parent
        joint.__set_parent(self)

        # Add Child
        self.__children.append(joint)

    def get_children(self) -> list["LollipopJoint"]:
        """
        returns
            Lollipopjoint
        """
        return self.__children

    def get_length(self) -> float:
        """
        returns
            float
        """
        return self.__length

    def get_parent(self) -> "LollipopJoint":
        """
        returns
            LollipopJoint
        """

        return self.__parent

    def get_root(self) -> "LollipopJoint":
        """
        returns
            OrbitJoint
        """

        joint = self
        while joint.get_parent() is not None:
            joint = joint.get_parent()

        return joint

    def get_rotation(self) -> float:
        """
        returns
            float
        """
        return self.__rotation

    def get_width(self) -> float:
        """
        returns
            float
        """
        return self.__width

    def get_z_offset(self) -> float:
        """
        returns
            float
        """
        return self.__z_offset

    def has_shape(self) -> bool:
        """
        returns
            bool
        """
        return self.__width > 0.0

    def is_joint_in_children(self, joint: "LollipopJoint") -> bool:
        """
        returns
            bool
        """
        type_validation(joint, LollipopJoint)

        if joint == self:
            return True

        found_in_child = False

        for child in self.__children:
            found_in_child = child.is_joint_in_children(joint)
            if found_in_child:
                break

        return found_in_child

    def render(self, start: Vector2f, debug: bool = False) -> None:
        """
        parameters
            Vector2f
        """
        type_validation([start, debug], [Vector2f, bool])

        # Return shape
        shape = Shape(VertexPositionNormalTexture)

        # Get Rotation as Velocity
        end = get_vector2f_of_angle(self.__rotation)
        end *= self.__length
        end += start

        start_vf3 = Vector3f(start.X, start.Y, 0.0)
        end_vf3 = Vector3f(end.X, end.Y, 0.0)

        # Debug?
        if debug:
            # Circle
            circle = generate_circle(5.0, 5)
            circle.scale(0.1)
            circle.translate(end_vf3)
            shape.add(circle)

            # Shape
            stick_offset = get_vector2f_of_angle(self.__rotation + 90.0) * 0.1
            stick_offset_vf3 = Vector3f(stick_offset.X, stick_offset.Y, 0.0)
            stick = generate_quadrilateral(
                start_vf3 - stick_offset_vf3,
                start_vf3 + stick_offset_vf3,
                end_vf3 + stick_offset_vf3,
                end_vf3 - stick_offset_vf3,
            )
            stick.translate(Vector3f(0.0, 0.0, self.__z_offset))
            shape.add(stick)

        # Shape?
        elif self.__width > 0.0:
            # Buffer
            buffer = end_vf3 - start_vf3
            buffer = buffer.normalize() * 0.0

            # Shape
            offset = get_vector2f_of_angle(self.__rotation + 90.0) * (
                self.__width / 2.0
            )
            offset_vf3 = Vector3f(offset.X, offset.Y, 0.0)
            stick = generate_quadrilateral(
                (start_vf3 - buffer) - offset_vf3,
                (start_vf3 - buffer) + offset_vf3,
                (end_vf3 + buffer) + offset_vf3,
                (end_vf3 + buffer) - offset_vf3,
            )
            stick.translate(Vector3f(0.0, 0.0, self.__z_offset))
            shape.add(stick)

        # Children
        for joint in self.__children:
            shape.add(joint.render(end, debug))

        # Return
        return shape

    def __set_parent(self, parent: "LollipopJoint") -> None:
        """
        parameters
            LollipopJoint/None
        """
        type_validation(parent, LollipopJoint)

        self.__parent = parent

    def set_rotation(self, rotation: float) -> None:
        """
        parameters
            float
            float
            float
        """

        type_validation(rotation, float)

        self.__rotation = rotation

    def set_z_offset(self, z_offset: float) -> None:
        """
        parameters
            flaot
        """
        type_validation(z_offset, float)

        self.__z_offset = z_offset
