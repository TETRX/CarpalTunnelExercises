from time import sleep

class ExerciseSession:
    def __init__(self, reps, instruction_display, exercise_func, img_dir = "../../../img/ex4a/"):
        self.reps = reps
        self.instruction_display = instruction_display
        self.ex_func = exercise_func
        self.img_dir = img_dir

    def run(self):
        self.instruction_display.mark_ready()
        for _ in range(self.reps):
            for hand in ["Right", "Left"]:
                self.ex_func(hand, self.instruction_display, img_dir=self.img_dir)
        sleep(1)
        self.instruction_display.close_window()
