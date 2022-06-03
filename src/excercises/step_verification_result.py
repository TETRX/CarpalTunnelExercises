from enum import Enum


class StepVerificationResult(Enum):
    IN_PROGRESS = 0
    FAILURE = 1
    SUCCESS = 2
