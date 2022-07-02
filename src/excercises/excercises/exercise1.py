from src.excercises.exercise import WristExercise
from src.excercises.instruction import Instruction
from src.excercises.instruction_display import TKInstructionDisplay, SimpleInstructionDisplay
from src.excercises.steps.angle_constraint import WristAngleConstraint
from src.excercises.steps.angle_constraint_hold_step import WristAngleConstraintHoldStep
from src.excercises.steps.angle_constraint_step import WristAngleConstraintStep
from src.excercises.steps.hand_in_frame_step import HandInFrameStep


def exercise1(which_hand: str, instruction_display):
    hold_time = 15
    hold_message = f"Hold this position for {hold_time} seconds"
    step1_constraints = []

    step1_constraints.append(
        WristAngleConstraint(angle=95, smaller=True),
    )
    step1_constraints.append(
        WristAngleConstraint(angle=85, smaller=False),
    )

    step1 = WristAngleConstraintStep(which_hand, Instruction("With your hand in front of you and your elbow straight, "
                                                  "bend your wrist down 90 degrees", None),
                                    step1_constraints
                                    )

    step1_hold_constraints = []

    step1_hold_constraints.append(
        WristAngleConstraint(
            angle=95,
            smaller=True
            ),
    )
    step1_hold_constraints.append(
        WristAngleConstraint(
            angle=75,
            smaller=False
            ),
    )
    step1_hold = WristAngleConstraintHoldStep(which_hand,
                                             Instruction(hold_message, None), hold_time,
                                             step1_hold_constraints
                                             )
    step2_constraints = []

    step2_constraints.append(
        WristAngleConstraint(angle=95, smaller=True),
    )
    step2_constraints.append(
        WristAngleConstraint(angle=85, smaller=False),
    )

    step2 = WristAngleConstraintStep(which_hand, Instruction("Now perform the same excercise but bend your wrist the "
                                                             "other way. With your hand in front of you and your elbow "
                                                             "straight, "
                                                  "bend your wrist up 90 degrees", None),
                                    step2_constraints
                                    )

    step2_hold_constraints = []

    step2_hold_constraints.append(
        WristAngleConstraint(
            angle=95,
            smaller=True
            ),
    )
    step2_hold_constraints.append(
        WristAngleConstraint(
            angle=75,
            smaller=False
            ),
    )
    step2_hold = WristAngleConstraintHoldStep(which_hand,
                                             Instruction(hold_message, None), hold_time,
                                             step2_hold_constraints
                                             )
    steps = [HandInFrameStep(which_hand),
             step1, step1_hold, step2, step2_hold,
             ]
    exercise = WristExercise(steps, instruction_display)

    exercise.run()


if __name__ == '__main__':
    instruction_display = SimpleInstructionDisplay()
    exercise1("Left", instruction_display)