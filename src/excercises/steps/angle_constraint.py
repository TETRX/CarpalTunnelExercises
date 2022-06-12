from src.excercises.hand_analysis.compute_angle import Finger, Joint, compute_joint_angle


class AngleConstraint:
    def __init__(self, angle, finger: Finger, joint: Joint, smaller: bool):
        self.finger = finger
        self.angle = angle
        self.joint = joint
        self.smaller = smaller

    def verify(self, hands, which_hand: str):
        angle = compute_joint_angle(hands, which_hand, self.finger, self.joint)
        if self.smaller:
            result = angle < self.angle
        else:
            result = angle > self.angle

        # if not result:
        #     print(f"Finger {self.finger}, joint {self.joint}, angle {angle}")

        return result
