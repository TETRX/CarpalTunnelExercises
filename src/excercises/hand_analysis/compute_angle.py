from enum import Enum, IntEnum
from typing import NamedTuple

from google.protobuf.json_format import MessageToDict
from mediapipe.python.solutions.holistic import PoseLandmark, HandLandmark
import numpy as np


class Finger(IntEnum):
    THUMB = HandLandmark.THUMB_CMC
    INDEX = HandLandmark.INDEX_FINGER_MCP
    MIDDLE = HandLandmark.MIDDLE_FINGER_MCP
    RING = HandLandmark.RING_FINGER_MCP
    PINKY = HandLandmark.PINKY_MCP


class Joint(IntEnum):
    FIRST = 0
    SECOND = 1
    THIRD = 2


def compute_joint_angle(hands: NamedTuple, which_hand: str, finger: Finger, joint: Joint):
    """

    :param hands: Return value of MediaPipe.Hands.process(image)
    :param which_hand: Either 'right' or 'left'
    :param finger: Enum specifying which finger is the constraint for; numeration is consistent with MediaPipe hand landmark model https://google.github.io/mediapipe/solutions/hands.html#hand-landmark-model
    :param joint: Enum specifying which joint is the constraint for; numeration is consistent with MediaPipe hand landmark model https://google.github.io/mediapipe/solutions/hands.html#hand-landmark-model
    :return:
    """
    for hand, handedness in zip(hands.multi_hand_world_landmarks, hands.multi_handedness):
        handedness = MessageToDict(handedness)
        hand_which_hand = handedness["classification"][0]["label"]
        if hand_which_hand == which_hand:
            '''
            establish three points abc that will for the angle
            the convention will be:
             - a is the point lowest on the hand, i.e.: closest to the forearm
             - b is the point in which the joint is
             - c is the point highest on the hand, i.e.: closest to fingertips
            '''

            # first get which landmarks of the hand a,b,c should be
            if joint == Joint.FIRST:  # if the joint is first, a will always be wrist
                a = HandLandmark.WRIST
            else:
                a = finger+joint-1
            b = finger+joint
            c = finger+joint+1

            #  now get their respective coordinates
            points_in_3d_space = {}
            for landmark in [a, b, c]:
                points_in_3d_space[landmark] = (np.array(
                    [
                        hand.landmark[landmark].x,
                        hand.landmark[landmark].y,
                        hand.landmark[landmark].z
                    ]
                ))

            # compute the angle
            ba = points_in_3d_space[a]-points_in_3d_space[b]
            bc = points_in_3d_space[c]-points_in_3d_space[b]

            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            angle = np.arccos(cosine_angle)

            return np.degrees(angle)


def compute_wrist_angle(results, which_hand: str):
    """

    :param results: Return value of MediaPipe.Holistic.process(image)
    :param which_hand: Either 'right' or 'left'
    :return:
    """
    hand = results.left_hand_landmarks if which_hand == "Left" else results.right_hand_landmarks
    pose = results.pose_landmarks
    if hand:
        '''
        establish three points abc that will for the angle
        the convention will be:
         - a is the point on the forearm
         - b is the point at the wrist joint
         - c is the point highest on the hand, i.e.: closest to fingertips
        '''

        # first get which landmarks of the hand a,b,c should be
        a = PoseLandmark.LEFT_ELBOW if which_hand == "Left" else PoseLandmark.RIGHT_ELBOW
        b = PoseLandmark.LEFT_WRIST if which_hand == "Left" else PoseLandmark.RIGHT_WRIST
        c = HandLandmark.MIDDLE_FINGER_TIP

        #  now get their respective coordinates
        points_in_2d = {}
        for landmark in [a, b]:
            points_in_2d[landmark] = (np.array(
                [
                    pose.landmark[landmark].x,
                    pose.landmark[landmark].y,
                ]
            ))
        points_in_2d[c] = (np.array(
            [
                hand.landmark[c].x,
                hand.landmark[c].y,
            ]
        ))

        # compute the angle
        ba = points_in_2d[a]-points_in_2d[b]
        bc = points_in_2d[c]-points_in_2d[b]

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)

        return np.degrees(angle)






