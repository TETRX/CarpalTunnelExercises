import asyncio
import datetime

from desktop_notifier import DesktopNotifier,Button
from src.excercises.excercises.exercise4a import exercise4a
from src.excercises.excercises.exercise_session import ExerciseSession
from src.excercises.instruction_display import SimpleInstructionDisplay


class ScheduledExercise:
    MESSAGE = 'According to your selected schedule, you are due for an exercise. Remember, these exercises should not cause you pain. If you have any questions, please consult your physician.'

    def __init__(self, exercise_func, scheduled_time: datetime.datetime, notifier: DesktopNotifier,
                 progress: asyncio.Future, instruction_display, img_dir = "../../img/", reps=1, addtitonal_info=None):
        self.session = ExerciseSession(reps, instruction_display, exercise_func, img_dir=img_dir)
        self.exercise_func = exercise_func
        self.scheduled_time = scheduled_time
        self.notifier = notifier
        self.progress = progress

        if addtitonal_info:
            self.message = f'{ScheduledExercise.MESSAGE}\n\nADDITIONAL_INFO: {addtitonal_info}'
        else:
            self.message = ScheduledExercise.MESSAGE


    async def notify(self):
        await self.notifier.send(title='Time for a hand exercise!', message=self.message,
                                buttons=[
                                    Button(
                                        title="Start exercise",
                                        on_pressed=self.run_exercise
                                    )
                                ]
                                )

    def run_exercise(self):
        self.session.run()
        self.progress.set_result(0)

if __name__ == '__main__':
    ex = ScheduledExercise(exercise4a, datetime.datetime.now()+datetime.timedelta(seconds=2), DesktopNotifier(), asyncio.Future(), SimpleInstructionDisplay())
    loop = asyncio.get_event_loop()
    loop.create_task(ex.notify())
    loop.run_until_complete(ex.progress)
