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


def exercise4b(hand):
    hold_message = "Hold this position for 3 seconds"
    non_thumb_fingers = [finger for finger in Finger if finger != Finger.THUMB]
    step1_constraints = []
    for finger in non_thumb_fingers:
        step1_constraints.append(
            HandAngleConstraint(140, finger, Joint.FIRST, False)
        )
        step1_constraints.append(
            HandAngleConstraint(145, finger, Joint.SECOND, False)
        )
        step1_constraints.append(
            HandAngleConstraint(140, finger, Joint.THIRD, False)
        )

    step1_constraints.append(
        HandAngleConstraint(120, Finger.THUMB, Joint.SECOND, False)
    )
    step1_constraints.append(
        HandAngleConstraint(120, Finger.THUMB, Joint.SECOND, False)
    )

    step1 = HandAngleConstraintStep(hand, Instruction("With your hand in front of you and your wrist straight, "
                                                  "fully straighten all of your fingers", None),
                                    step1_constraints
                                    )
    step1_hold = HandAngleConstraintHoldStep(hand,
                                             Instruction(hold_message, None), 3,
                                             step1_constraints
                                             )

    step2_constraints = []
    for finger in non_thumb_fingers:
        step2_constraints.append(
            HandAngleConstraint(150, finger, Joint.FIRST, True)
        )
        step2_constraints.append(
            HandAngleConstraint(140, finger, Joint.SECOND, False)
        )
        step2_constraints.append(
            HandAngleConstraint(140, finger, Joint.THIRD, False)
        )

    step2 = HandAngleConstraintStep(hand, Instruction(
        "Make a “tabletop” with your fingers by bending at your bottom knuckle and keeping the fingers straight ",
        None),
                                    step2_constraints
                                    )
    step2_hold = HandAngleConstraintHoldStep(hand, Instruction(hold_message, None), 3,
                                             step2_constraints
                                             )

    step3_constraints = []
    for finger in non_thumb_fingers:
        step3_constraints.append(
            HandAngleConstraint(160, finger, Joint.FIRST, True)
        )
        step3_constraints.append(
            HandAngleConstraint(140, finger, Joint.SECOND, True)
        )
        step3_constraints.append(
            HandAngleConstraint(100, finger, Joint.THIRD, False)
        )

    step3 = HandAngleConstraintStep(hand, Instruction(
        "Bend your fingers at the middle joint, touching your fingers to your palm ", None),
                                    step3_constraints
                                    )
    step3_hold = HandAngleConstraintHoldStep(hand, Instruction(hold_message, None), 4,
                                             step3_constraints
                                             )

    steps = [HandInFrameStep(hand),
             step1, step1_hold,
             step2, step2_hold,
             step3, step3_hold
             ]
    instruction_display = InstructionDisplay()
    exercise = HandExercise(steps, instruction_display)

    exercise.run()


if __name__ == '__main__':
    exercise4b("Right")
