from src.excercises.exercise import (
    Exercise,
    HandExercise,
)
from src.excercises.hand_analysis.compute_angle import Finger, Joint
from src.excercises.instruction import Instruction
from src.excercises.instruction_display import InstructionDisplay
from src.excercises.steps.angle_constraint import HandAngleConstraint
from src.excercises.steps.angle_constraint_hold_step import HandAngleConstraintHoldStep
from src.excercises.steps.angle_constraint_step import HandAngleConstraintStep
from src.excercises.steps.fake_step import FakeHandStep
from src.excercises.steps.hand_in_frame_step import HandInFrameStep


def exercise3(hand):
    hold_time = 3  # in seconds
    hold_message = f"Hold this position for {hold_time} seconds"
    non_thumb_fingers = [finger for finger in Finger if finger != Finger.THUMB]
    straight_fingers_step_constraints = []
    for finger in non_thumb_fingers:
        straight_fingers_step_constraints.append(
            HandAngleConstraint(140, finger, Joint.FIRST, False)
        )
        straight_fingers_step_constraints.append(
            HandAngleConstraint(145, finger, Joint.SECOND, False)
        )
        straight_fingers_step_constraints.append(
            HandAngleConstraint(140, finger, Joint.THIRD, False)
        )

    straight_fingers_step_constraints.append(
        HandAngleConstraint(120, Finger.THUMB, Joint.SECOND, False)
    )

    straight_fingers_step = HandAngleConstraintStep(hand, Instruction("With your hand in front of you and your wrist "
                                                               "straight, "
                                                  "fully straighten all of your fingers", None),
                                    straight_fingers_step_constraints
                                    )
    straight_fingers_step_hold = HandAngleConstraintHoldStep(hand,
                                             Instruction(hold_message, None), hold_time,
                                             straight_fingers_step_constraints
                                             )

    thumb_step_constraints = []
    for finger in non_thumb_fingers:
        thumb_step_constraints.append(
            HandAngleConstraint(140, finger, Joint.FIRST, False)
        )
        thumb_step_constraints.append(
            HandAngleConstraint(145, finger, Joint.SECOND, False)
        )
        thumb_step_constraints.append(
            HandAngleConstraint(140, finger, Joint.THIRD, False)
        )

    thumb_step_constraints.append(
        HandAngleConstraint(
            165,
            Finger.THUMB,
            Joint.SECOND,
            False
            )
    )
    thumb_step_constraints.append(
        HandAngleConstraint(
            155,
            Finger.THUMB,
            Joint.THIRD,
            False
            )
    )
    thumb_step_constraints.append(
        HandAngleConstraint(
            180,
            Finger.THUMB,
            Joint.THIRD,
            True
            )
    )

    thumb_step = HandAngleConstraintStep(hand, Instruction(
        "Stretch your thumb out to the side while keeping your other fingers straight ", None),
                                    thumb_step_constraints
                                    )
    thumb_step_hold = HandAngleConstraintHoldStep(hand, Instruction(hold_message, None), hold_time,
                                             thumb_step_constraints
                                             )

    fist_step_constraints = []
    for finger in non_thumb_fingers:
        fist_step_constraints.append(
            HandAngleConstraint(160, finger, Joint.FIRST, True)
        )
        fist_step_constraints.append(
            HandAngleConstraint(140, finger, Joint.SECOND, True)
        )
        fist_step_constraints.append(
            HandAngleConstraint(160, finger, Joint.THIRD, True)
        )

    fist_step_constraints.append(
        HandAngleConstraint(170, Finger.THUMB, Joint.FIRST, True)
    )
    fist_step_constraints.append(
        HandAngleConstraint(170, Finger.THUMB, Joint.SECOND, True)
    )

    fist_step_constraints.append(
        HandAngleConstraint(150, Finger.THUMB, Joint.THIRD, True)
    )

    fist_step = HandAngleConstraintStep(hand, Instruction(
        "Make a tight fist with your thumb over your fingers", None),
                                    fist_step_constraints
                                    )
    fist_step_hold = HandAngleConstraintHoldStep(hand, Instruction(hold_message, None), hold_time,
                                             fist_step_constraints
                                             )

    steps = [HandInFrameStep(hand),
             fist_step, fist_step_hold,
             straight_fingers_step, straight_fingers_step_hold,
             thumb_step, thumb_step_hold,
             ]
    instruction_display = InstructionDisplay()
    exercise = HandExercise(steps, instruction_display)

    exercise.run()


if __name__ == '__main__':
    exercise3("Right")
