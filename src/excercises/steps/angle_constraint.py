from typing import NamedTuple

from src.excercises.hand_analysis.compute_angle import (
    Finger,
    Joint,
    compute_joint_angle,
    compute_wrist_angle,
)


class AngleConstraint:
    def verify(self, results: NamedTuple, which_hand: str) -> bool:
        """
        Return True if results for the specified hand satisfy the constraint

        :param results: Return value of MediaPipe.Hands.process(img)
        :param which_hand: Either 'right' or 'left'
        :return: True if the constraint is satisfied
        """
        raise NotImplementedError


class HandAngleConstraint(AngleConstraint):
    def __init__(self, angle, finger: Finger, joint: Joint, smaller: bool):
        """
        Declare an angle constraint for a specified joint of a specified finger.

        :param angle: Value of the constraint
        :param finger: Enum specifying which finger is the constraint for; numeration is consistent with MediaPipe hand landmark model https://google.github.io/mediapipe/solutions/hands.html#hand-landmark-model
        :param joint: Enum specifying which joint is the constraint for; numeration is consistent with MediaPipe hand landmark model https://google.github.io/mediapipe/solutions/hands.html#hand-landmark-model
        :param smaller: True if constraint angle should be smaller than the specified value
        """
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
        """
        Declare an angle constraint for the wrist joint.

        :param angle: Value of the constraint
        :param smaller: True if constrained angle should be smaller than the specified value
        """
        self.angle = angle
        self.smaller = smaller

    def verify(self, results: NamedTuple, which_hand: str) -> bool:
        angle = compute_wrist_angle(results, which_hand)
        if self.smaller:
            result = angle < self.angle
        else:
            result = angle > self.angle
        return result
