from typing import NamedTuple

from src.excercises.instruction import Instruction
from src.excercises.step import Step
from src.excercises.step_verification_result import StepVerificationResult
from google.protobuf.json_format import MessageToDict


class HandInFrameStep(Step):  # prompts us to get our hand in frame. We can pad each step with this since this seems
    # like the most likely failure scenario
    def __init__(self, which_hand: str):
        """
        Declare that specified hand should be visible in frame.

        :param which_hand: Either 'right' or 'left'
        """
        super().__init__(Instruction(f"Position yourself so that your "
                                     f"{which_hand.lower()} hand is visible in your camera.",
                              None  # TODO
                              ))
        self.which_hand = which_hand

    def verify(self, results: NamedTuple):
        """

        :param results: Return value of MediaPipe.Hands.process(image)
        :return:
        """
        if hasattr(results, "left_hand_landmarks") and (results.left_hand_landmarks is not None and self.which_hand ==
                                                 "Left") or (hasattr(results, "left_hand_landmarks") and
                results.right_hand_landmarks is
                                                                                        not None and self.which_hand
                                                                                        == "Right"):
            return StepVerificationResult.SUCCESS
        elif hasattr(results, "multi_handedness") and results.multi_handedness is not None:
            for classification in results.multi_handedness:
                handedness = MessageToDict(classification)
                if handedness["classification"][0]["label"] == self.which_hand:
                    return StepVerificationResult.SUCCESS
        return StepVerificationResult.IN_PROGRESS
