"""
entity.py
"""

from ...ext.pyHelpers.files import dump_json_data
from ...ext.pyHelpers.trigonometry import get_velocity_of_angle
from ...ext.pyHelpers.type_validation import type_validation
from ...ext.pyMultiD.vector import Vector2f

from .lollipop_joint import LollipopJoint


class Entity:
    """
    Base for a Entity
    """

    __slots__ = ["__frames", "__joints", "__root"]

    def __init__(self) -> None:
        self.__frames = []
        self.__joints = {}
        self.__root = None

    def add(self, name: str, joint: "LollipopJoint") -> None:
        """
        parameters
            string
            LollipopJoint
        """

        type_validation([name, joint], [str, LollipopJoint])

        if name not in self.__joints:
            self.__joints[name] = joint

    def create_frame(self, name: str) -> None:
        """
        Creates a Frame from the Entity's current
        rotations.
        """

        if self.__root == None:
            raise ValueError("Root must be set before creating Frames.")

        # Here we iterate our and root and its children, grabbing...
        # Wait.  We need to reference our ids we created.  Crap.
        # Can we do a reverse lookup?  Given a Lollipop find its id?
        def get_rotation_and_offset(joint: LollipopJoint, start: Vector2f) -> []:
            data = []

            if joint.has_shape():
                data.append(
                    {
                        "name": self.get_name(joint),
                        "offsetX": round(start.X, 2),
                        # When building shapes, we center on origin.  Offset X is centered,
                        # so we need to do the same with Offset Y.
                        "offsetY": round(start.Y - (joint.get_length() * 0.5), 2),
                        "offsetZ": round(joint.get_z_offset(), 2),
                        "rotation": joint.get_rotation(),
                    }
                )

            end = get_velocity_of_angle(joint.get_rotation())
            end *= joint.get_length()
            end += start

            for child in joint.get_children():
                data.extend(get_rotation_and_offset(child, end))

            return data

        # Frame Data
        frame_data = get_rotation_and_offset(self.__root, Vector2f(0.0, 0.0))

        # Get Minimum/Maximum
        minimum = Vector2f(999999.0, 999999.0)
        maximum = Vector2f(-999999.0, -999999.0)
        for frame in frame_data:
            minimum.X = min(frame["offsetX"], minimum.X)
            minimum.Y = min(frame["offsetY"], minimum.Y)
            maximum.X = max(frame["offsetX"], maximum.X)
            maximum.Y = max(frame["offsetY"], maximum.Y)

        # We want the diagonal, then we'll modify our frame data
        diagonal = maximum - minimum
        diagonal_half = diagonal * 0.5
        for frame in frame_data:
            frame["offsetX"] += diagonal_half.X
            frame["offsetY"] += diagonal_half.Y

        # Add the Frame
        self.__frames.append(
            {
                "name": name,
                "data": frame_data,
            }
        )

    def export(self, file_name: str, path: str) -> None:
        """
        parameters
            str
            str
        """

        json = {"name": file_name, "parts": [], "frames": self.__frames}

        for name in self.__joints:
            joint = self.get(name)
            if joint.has_shape():
                json["parts"].append(
                    {
                        "name": name,
                        "length": joint.get_length(),
                        "width": joint.get_width(),
                    }
                )

        dump_json_data(file_name, path, json)

    def get(self, name: str) -> LollipopJoint:
        """
        parameters
            str
        returns
            joint
        """

        # No need to Type Validate, has does that.
        if self.has(name):
            return self.__joints[name]

        return None

    def get_name(self, joint: LollipopJoint) -> str | None:
        """
        parameters
            LollipopJoint
        returns
            str | None
        """
        for name in self.__joints:
            if self.__joints[name] == joint:
                return name

        return None

    def has(self, name: str) -> bool:
        """
        parameter
            str
        returns
            bool
        """

        type_validation(name, str)

        return name in self.__joints

    def link(self, child: str, parent: str) -> bool:
        """
        parameters
            str
            str
        returns
            bool
        """

        type_validation([child, parent], str)

        if child in self.__joints and parent in self.__joints:
            self.__joints[parent].add(self.__joints[child])
            return True

        return False

    def set_root(self, root: LollipopJoint) -> None:
        """
        parameters
            LollipopJoint
        """
        type_validation(root, LollipopJoint)

        self.__root = root
