from src.excercises.exercise import WristExercise
from src.excercises.instruction import Instruction
from src.excercises.instruction_display import InstructionDisplay
from src.excercises.steps.angle_constraint import WristAngleConstraint
from src.excercises.steps.angle_constraint_hold_step import WristAngleConstraintHoldStep
from src.excercises.steps.angle_constraint_step import WristAngleConstraintStep
from src.excercises.steps.hand_in_frame_step import HandInFrameStep


def exercise1(which_hand: str):
    hold_message = "Hold this position for 3 seconds"
    step1_constraints = []

    step1_constraints.append(
        WristAngleConstraint(120, False)
    )
    step1_constraints.append(
        WristAngleConstraint(120, False)
    )

    step1 = WristAngleConstraintStep(which_hand, Instruction("With your hand in front of you and your wrist straight, "
                                                  "fully straighten all of your fingers", None),
                                    step1_constraints
                                    )
    step1_hold = WristAngleConstraintHoldStep(which_hand,
                                             Instruction(hold_message, None), 3,
                                             step1_constraints
                                             )

    step2_constraints = []

    step2 = WristAngleConstraintStep(which_hand, Instruction(
        "Bend the tips of your fingers into the “hook” position with your knuckles pointing up ", None),
                                    step2_constraints
                                    )
    step2_hold = WristAngleConstraintHoldStep(which_hand, Instruction(hold_message, None), 3,
                                             step2_constraints
                                             )

    steps = [HandInFrameStep(which_hand),
             step1, step1_hold,
             step2, step2_hold,
             ]
    instruction_display = InstructionDisplay()
    exercise = WristExercise(steps, instruction_display)

    exercise.run()


if __name__ == '__main__':
    exercise1("Right")