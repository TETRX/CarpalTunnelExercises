import asyncio
import os.path
from time import sleep

from src.excercises.exercise import Exercise
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
from src.img.img_process import get_img


def exercise4a(hand, instruction_display, img_dir="../../../img/ex4a/"):
    img1 = get_img(os.path.abspath(os.path.join(img_dir, "ex4a_1.png")))
    img2 = get_img(os.path.join(img_dir, "ex4a_2.png"))
    img3 = get_img(os.path.join(img_dir, "ex4a_3.png"))

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
            HandAngleConstraint(130, finger, Joint.FIRST, False)
        )
        step2_constraints.append(
            HandAngleConstraint(140, finger, Joint.SECOND, True)
        )
        step2_constraints.append(
            HandAngleConstraint(160, finger, Joint.THIRD, True)
        )

    step2 = HandAngleConstraintStep(hand, Instruction(
        "Bend the tips of your fingers into the “hook” position with your knuckles pointing up ", None),
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
            HandAngleConstraint(160, finger, Joint.THIRD, True)
        )

    step3_constraints.append(
        HandAngleConstraint(170, Finger.THUMB, Joint.FIRST, True)
    )
    step3_constraints.append(
        HandAngleConstraint(170, Finger.THUMB, Joint.SECOND, True)
    )

    step3_constraints.append(
        HandAngleConstraint(150, Finger.THUMB, Joint.THIRD, True)
    )

    step3 = HandAngleConstraintStep(hand, Instruction(
        "Make a tight fist with your thumb over your fingers", None),
                                    step3_constraints
                                    )
    step3_hold = HandAngleConstraintHoldStep(hand, Instruction(hold_message, None), 3,
                                             step3_constraints
                                             )

    steps = [HandInFrameStep(hand),
             step1, step1_hold,
             step2, step2_hold,
             step3, step3_hold
             ]
    instruction_display.mark_ready()
    exercise = Exercise(steps, instruction_display)

    exercise.run()


if __name__ == '__main__':
    from threading import Thread
    success_image = get_img(os.path.join("../../../img/ex4a/",".." ,"success.png"))

    display = InstructionDisplay(success_image=success_image)

    def _run_ex_and_exit(*args):
        exercise4a(*args)
        sleep(1)
        display.close_window()

    thread = Thread(target=_run_ex_and_exit, args = ("Right", display))
    thread.start()
    display.run()
