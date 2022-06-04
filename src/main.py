from src.excercises.exercise import Exercise
from src.excercises.hand_analysis.compute_angle import Finger, Joint
from src.excercises.instruction import Instruction
from src.excercises.instruction_display import InstructionDisplay
from src.excercises.steps.angle_constraint import AngleConstraint
from src.excercises.steps.angle_constraint_hold_step import AngleConstraintHoldStep
from src.excercises.steps.angle_constraint_step import AngleConstraintStep
from src.excercises.steps.fake_step import FakeStep
from src.excercises.steps.hand_in_frame_step import HandInFrameStep


def main():
    non_thumb_fingers = [finger for finger in Finger if finger != Finger.THUMB]
    ex4a_step2_constraints = []
    for finger in non_thumb_fingers:
        ex4a_step2_constraints.append(
            AngleConstraint(130, finger, Joint.FIRST, False)
        )
        ex4a_step2_constraints.append(
            AngleConstraint(140, finger, Joint.SECOND, True)
        )
        ex4a_step2_constraints.append(
            AngleConstraint(160, finger, Joint.THIRD, True)
        )

    ex4a_step2 = AngleConstraintStep("Right", Instruction("Curl your fingers",None),
                                     ex4a_step2_constraints
                                     )
    ex4a_step2_hold = AngleConstraintHoldStep("Right",  Instruction("Keep your fingers curled",None), 4,
                                              ex4a_step2_constraints
                                              )

    steps = [HandInFrameStep("Right"), ex4a_step2, ex4a_step2_hold]
    instruction_display = InstructionDisplay()
    exercise = Exercise(steps, instruction_display)

    exercise.run()


if __name__ == '__main__':
    main()
