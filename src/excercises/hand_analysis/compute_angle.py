from enum import Enum, IntEnum

from google.protobuf.json_format import MessageToDict
from mediapipe.python.solutions.hands import HandLandmark
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


def compute_joint_angle(hands, which_hand: str, finger, joint):
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









