from src.excercises.exercise import Exercise
from src.excercises.instruction_display import InstructionDisplay
from src.excercises.steps.fake_step import FakeStep
from src.excercises.steps.hand_in_frame_step import HandInFrameStep


def main():
    steps = [HandInFrameStep("Right"), FakeStep("Right")]
    instruction_display = InstructionDisplay()
    excercise = Exercise(steps,instruction_display)

    excercise.run()

if __name__ == '__main__':
    main()
