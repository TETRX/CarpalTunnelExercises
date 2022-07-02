from datetime import datetime, timedelta

from src.excercises.step import Step
from src.excercises.step_verification_result import StepVerificationResult
from google.protobuf.json_format import MessageToDict


class HandConstraintHoldStep(Step):
    def __init__(self, which_hand: str, instruction, hold_time, constraints):
        super().__init__(instruction)
        self.which_hand = which_hand
        self.time_started_step = None
        self.hold_time = hold_time
        self.constraints = constraints

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
                        break

                    if timedelta(seconds=5) <= (datetime.now()-self.time_started_step):
                        return StepVerificationResult.SUCCESS
                    return StepVerificationResult.IN_PROGRESS

        self.time_started_step = None
        return StepVerificationResult.FAILURE


class WristConstraintHoldStep(Step):
    def __init__(self, which_hand: str, instruction, hold_time, constraints):
        super().__init__(instruction)
        self.which_hand = which_hand
        self.time_started_step = None
        self.hold_time = hold_time
        self.constraints = constraints

    def verify(self, results):
        if (results.left_hand_landmarks is not None and self.which_hand == "Left") or (results.right_hand_landmarks is
                                                                                       not \
                None and self.which_hand == "Right"):
            if self.time_started_step is None:
                self.time_started_step = datetime.now()

            constraints_hold = True
            for constraint in self.constraints:
                if not constraint.verify(results, self.which_hand):
                    constraints_hold = False

            if not constraints_hold:
                self.time_started_step = None
                return StepVerificationResult.FAILURE

            if timedelta(seconds=5) <= (datetime.now()-self.time_started_step):
                return StepVerificationResult.SUCCESS
            return StepVerificationResult.IN_PROGRESS

        self.time_started_step = None
        return StepVerificationResult.FAILURE