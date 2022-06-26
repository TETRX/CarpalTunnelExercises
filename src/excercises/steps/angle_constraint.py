from typing import NamedTuple

from src.excercises.hand_analysis.compute_angle import (
    Finger,
    Joint,
    compute_joint_angle,
    compute_wrist_angle,
)


class AngleConstraint:
    def verify(self, results: NamedTuple, which_hand: str) -> bool:
        raise NotImplementedError


class HandAngleConstraint(AngleConstraint):
    def __init__(self, angle, finger: Finger, joint: Joint, smaller: bool):
        self.finger = finger
        self.angle = angle
        self.joint = joint
        self.smaller = smaller

    def verify(self, results: NamedTuple, which_hand: str) -> bool:
        angle = compute_joint_angle(results, which_hand, self.finger, self.joint)
        if self.smaller:
            result = angle < self.angle
        else:
            result = angle > self.angle
        return result


class WristAngleConstraint(AngleConstraint):
    def __init__(self, angle, smaller: bool):
        self.angle = angle
        self.smaller = smaller

    def verify(self, results: NamedTuple, which_hand: str) -> bool:
        angle = compute_wrist_angle(results, which_hand)
        if self.smaller:
            result = angle < self.angle
        else:
            result = angle > self.angle
        return result
