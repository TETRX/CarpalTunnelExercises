from datetime import datetime, timedelta
from typing import NamedTuple

from src.excercises.hand_analysis.compute_angle import compute_joint_angle, Finger, Joint
from src.excercises.instruction import Instruction
from src.excercises.step import Step
from src.excercises.step_verification_result import StepVerificationResult
from google.protobuf.json_format import MessageToDict


class FakeHandStep(Step): # keep your hand in frame for 2 seconds
    def __init__(self, which_hand: str):
        """

        :param which_hand: Either 'right' or 'left'
        """
        super().__init__(Instruction(f"Keep your "
                                     f"{which_hand.lower()} hand visible in your camera.",
                              None  # TODO
                              ))
        self.which_hand = which_hand
        self.time_started_step = None

    def verify(self, hands: NamedTuple):
        """

        :param hands: Results of running MediaPipe.Hands.process(image)
        :return:
        """
        if hands.multi_handedness is not None:
            for classification in hands.multi_handedness:
                handedness = MessageToDict(classification)

                if handedness["classification"][0]["label"] == self.which_hand:
                    if self.time_started_step is None:
                        self.time_started_step = datetime.now()

                    # print(compute_joint_angle(hands,self.which_hand,Finger.INDEX,Joint.SECOND))

                    if timedelta(seconds=2) <= (datetime.now()-self.time_started_step):
                        return StepVerificationResult.SUCCESS
                    return StepVerificationResult.IN_PROGRESS

        self.time_started_step = None
        return StepVerificationResult.FAILURE
