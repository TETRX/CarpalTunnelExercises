from typing import NamedTuple

from mediapipe.python.solutions.hands import HandLandmark
from mediapipe.python.solutions.pose import PoseLandmark


class HandDirectionConstraint:
    def __init__(self, points_up: bool):
        """
        Declare a constraint on the direction the hand is facing.

        :param points_up: True if hand should be pointing up
        """
        self.points_up = points_up

    def verify(self, results: NamedTuple, which_hand: str):
        """

        :param results: Return value of running MediaPipe.Hands.process(image)
        :param which_hand: Either 'right' or 'left'
        :return:
        """
        hand = results.left_hand_landmarks if which_hand == "Left" else results.right_hand_landmarks
        pose = results.pose_landmarks
        if hand:
            wrist = PoseLandmark.LEFT_WRIST if which_hand == "Left" else PoseLandmark.RIGHT_WRIST
            finger_tip = HandLandmark.MIDDLE_FINGER_TIP
            if self.points_up:
                return hand.landmark[finger_tip].y < pose.landmark[wrist].y
            else:
                return hand.landmark[finger_tip].y > pose.landmark[wrist].y


