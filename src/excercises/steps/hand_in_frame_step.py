from src.excercises.instruction import Instruction
from src.excercises.step import Step
from src.excercises.step_verification_result import StepVerificationResult
from google.protobuf.json_format import MessageToDict


class HandInFrameStep(Step):  # prompts us to get our hand in frame. We can pad each step with this since this seems
    # like the most likely failure scenario
    def __init__(self, which_hand: str):
        super().__init__(Instruction(f"Position yourself so that your "
                                     f"{which_hand.lower()} hand is visible in your camera.",
                              None  # TODO
                              ))
        self.which_hand = which_hand

    def verify(self, hands):
        if hands.multi_handedness is not None:
            for classification in hands.multi_handedness:
                handedness = MessageToDict(classification)
                if handedness["classification"][0]["label"] == self.which_hand:
                    return StepVerificationResult.SUCCESS
        return StepVerificationResult.IN_PROGRESS
