from datetime import datetime, timedelta

from src.excercises.instruction import Instruction
from src.excercises.step import Step
from src.excercises.step_verification_result import StepVerificationResult
from google.protobuf.json_format import MessageToDict

class FakeStep(Step): # keep your hand in frame for 2 seconds
    def __init__(self, which_hand: str):
        super().__init__(Instruction(f"Keep your "
                                     f"{which_hand.lower()} hand visible in your camera.",
                              None  # TODO
                              ))
        self.which_hand = which_hand
        self.time_started_step = None

    def verify(self, hands):
        if hands.multi_handedness is not None:
            for classification in hands.multi_handedness:
                handedness = MessageToDict(classification)

                if handedness["classification"][0]["label"] == self.which_hand:
                    if self.time_started_step is None:
                        self.time_started_step = datetime.now()

                    if timedelta(seconds=2) <= (datetime.now()-self.time_started_step):
                        return StepVerificationResult.SUCCESS
                    return StepVerificationResult.IN_PROGRESS

        self.time_started_step = None
        return StepVerificationResult.FAILURE
