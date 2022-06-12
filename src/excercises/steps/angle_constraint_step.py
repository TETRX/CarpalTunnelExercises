from datetime import datetime, timedelta

from src.excercises.step import Step
from src.excercises.step_verification_result import StepVerificationResult
from google.protobuf.json_format import MessageToDict


class AngleConstraintStep(Step):
    def __init__(self, which_hand: str, instruction, constraints, frames_to_start=3):
        super().__init__(instruction)
        self.which_hand = which_hand
        self.time_started_step = None
        self.constraints = constraints
        self.frames_to_start = 3
        self.frame_streak = 0

    def verify(self, hands):
        if hands.multi_handedness is not None:
            for classification in hands.multi_handedness:
                handedness = MessageToDict(classification)

                if handedness["classification"][0]["label"] == self.which_hand:
                    if self.time_started_step is None:
                        self.time_started_step = datetime.now()

                    constraints_hold = True
                    for constraint in self.constraints:
                        if not constraint.verify(hands, self.which_hand):
                            constraints_hold = False

                    if not constraints_hold:
                        self.frame_streak = 0
                        return StepVerificationResult.IN_PROGRESS
                    else:
                        self.frame_streak += 1
                        if self.frame_streak == self.frames_to_start:
                            return StepVerificationResult.SUCCESS
                        else:
                            return StepVerificationResult.IN_PROGRESS


        return StepVerificationResult.FAILURE
