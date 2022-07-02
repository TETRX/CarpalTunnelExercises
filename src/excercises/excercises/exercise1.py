import os

from src.excercises.exercise import WristExercise
from src.excercises.instruction import Instruction
from src.excercises.instruction_display import TKInstructionDisplay, SimpleInstructionDisplay
from src.excercises.steps.angle_constraint import WristAngleConstraint
from src.excercises.steps.constraint_hold_step import WristConstraintHoldStep
from src.excercises.steps.constraint_step import WristConstraintStep
from src.excercises.steps.hand_direction_constraint import HandDirectionConstraint
from src.excercises.steps.hand_in_frame_step import HandInFrameStep
from src.img.img_process import get_img


def exercise1(which_hand: str, instruction_display, img_dir="../../../img/"):
    img = get_img(os.path.join(img_dir, f'ex1/ex1.png'))
    hold_time = 15
    hold_message = f"Hold this position for {hold_time} seconds"
    step1_constraints = [WristAngleConstraint(angle=95, smaller=True), WristAngleConstraint(angle=85, smaller=False), HandDirectionConstraint(False)]

    step1 = WristConstraintStep(which_hand, Instruction(" Bend your wrist down 90 degrees"
                                                             "Use your opposite hand to apply gentle pressure across "
                                                             "the palm and pull it toward you until you feel a "
                                                             "stretch on the inside of your forearm.", img),
                                step1_constraints
                                )

    step1_hold_constraints = [WristAngleConstraint(
        angle=95,
        smaller=True
    ), WristAngleConstraint(
        angle=75,
        smaller=False
    )]

    step1_hold = WristConstraintHoldStep(which_hand,
                                         Instruction(hold_message, img), hold_time,
                                         step1_hold_constraints
                                         )

    steps = [HandInFrameStep(which_hand),
             step1, step1_hold
             ]
    exercise = WristExercise(steps, instruction_display)

    exercise.run()


if __name__ == '__main__':
    instruction_display = SimpleInstructionDisplay()
    exercise1("Left", instruction_display)
