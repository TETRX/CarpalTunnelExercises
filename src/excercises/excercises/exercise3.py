import os

from src.excercises.exercise import (
    Exercise,
    HandExercise,
)
from src.excercises.hand_analysis.compute_angle import Finger, Joint
from src.excercises.instruction import Instruction
from src.excercises.instruction_display import TKInstructionDisplay, SimpleInstructionDisplay
from src.excercises.steps.angle_constraint import HandAngleConstraint
from src.excercises.steps.constraint_hold_step import HandConstraintHoldStep
from src.excercises.steps.constraint_step import HandConstraintStep
from src.excercises.steps.fake_step import FakeHandStep
from src.excercises.steps.hand_in_frame_step import HandInFrameStep
from src.img.img_process import get_img


def exercise3(hand, instruction_display, img_dir="../../../img/"):
    img = [get_img(os.path.join(img_dir, f'ex3/ex3_{i}.png')) for i in range(1,7)]

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

    straight_fingers_step = HandConstraintStep(hand, Instruction("With your hand in front of you and your wrist "
                                                               "straight, "
                                                  "fully straighten all of your fingers", img[1]),
                                               straight_fingers_step_constraints
                                               )
    straight_fingers_step_hold = HandConstraintHoldStep(hand,
                                                        Instruction(hold_message, img[1]), hold_time,
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

    thumb_step = HandConstraintStep(hand, Instruction(
        "Stretch your thumb out to the side while keeping your other fingers straight ", img[5]),
                                    thumb_step_constraints
                                    )
    thumb_step_hold = HandConstraintHoldStep(hand, Instruction(hold_message, img[5]), hold_time,
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

    fist_step = HandConstraintStep(hand, Instruction(
        "Make a tight fist with your thumb over your fingers", img[0]),
                                   fist_step_constraints
                                   )
    fist_step_hold = HandConstraintHoldStep(hand, Instruction(hold_message, img[0]), hold_time,
                                            fist_step_constraints
                                            )

    steps = [HandInFrameStep(hand),
             fist_step, fist_step_hold,
             straight_fingers_step, straight_fingers_step_hold,
             thumb_step, thumb_step_hold,
             ]
    exercise = HandExercise(steps, instruction_display)

    exercise.run()


if __name__ == '__main__':
    instruction_display = SimpleInstructionDisplay()
    exercise3("Right", instruction_display)
