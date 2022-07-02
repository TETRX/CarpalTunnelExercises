from datetime import datetime, timedelta
from typing import List

from src.excercises.step import Step
from src.excercises.step_verification_result import StepVerificationResult
from google.protobuf.json_format import MessageToDict

from src.excercises.steps.angle_constraint import (
    AngleConstraint,
    WristAngleConstraint,
)


class HandConstraintStep(Step):
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


class WristConstraintStep(Step):
    def __init__(self, which_hand: str, instruction, constraints: List[AngleConstraint], frames_to_start=3):
        super().__init__(instruction)
        self.which_hand = which_hand
        self.time_started_step = None
        self.constraints = constraints
        self.frames_to_start = 3
        self.frame_streak = 0

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
                self.frame_streak = 0
                return StepVerificationResult.IN_PROGRESS
            else:
                self.frame_streak += 1
                if self.frame_streak == self.frames_to_start:
                    return StepVerificationResult.SUCCESS
                else:
                    return StepVerificationResult.IN_PROGRESS

        return StepVerificationResult.FAILURE