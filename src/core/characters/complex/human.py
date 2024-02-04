"""
human.py
"""

from ..lollipop_joint import LollipopJoint

from ..entity import Entity


def generate_human() -> Entity:
    """
    returns
        Entity
    """

    human = Entity()

    # joints
    human.add("head_human_large", LollipopJoint(1.0, 0.5, 270.0))
    human.add("left_shoulder_human_large", LollipopJoint(1.5, 0.0, 0.0))
    human.add("right_shoulder_human_large", LollipopJoint(1.5, 0.0, 180.0))
    human.add("torso_human_large", LollipopJoint(3.0, 2.0, 270.0))
    human.add("left_arm_human_large", LollipopJoint(4.5, 0.5, 270.0))
    human.add("right_arm_human_large", LollipopJoint(4.5, 0.5, 270.0))
    human.add("left_hip_human_large", LollipopJoint(0.8, 0.0, 0.0))
    human.add("right_hip_human_large", LollipopJoint(0.8, 0.0, 180.0))
    human.add("left_leg_human_large", LollipopJoint(6.0, 0.5, 270.0))
    human.add("right_leg_human_large", LollipopJoint(6.0, 0.5, 270.0))

    # put together
    human.link("left_shoulder_human_large", "head_human_large")
    human.link("right_shoulder_human_large", "head_human_large")
    human.link("torso_human_large", "head_human_large")
    human.link("left_arm_human_large", "left_shoulder_human_large")
    human.link("right_arm_human_large", "right_shoulder_human_large")
    human.link("left_hip_human_large", "torso_human_large")
    human.link("right_hip_human_large", "torso_human_large")
    human.link("left_leg_human_large", "left_hip_human_large")
    human.link("right_leg_human_large", "right_hip_human_large")

    # Return root Joint
    return human
