import asyncio
import datetime

from desktop_notifier import DesktopNotifier,Button
from src.excercises.excercises.exercise4a import exercise4a


class ScheduledExercise:
    MESSAGE = 'According to your selected schedule, you are due for an exercise. Remember, these exercises should not cause you pain. If you have any questions, please consult your physician.'

    def __init__(self, exercise_func, scheduled_time: datetime.datetime, notifier: DesktopNotifier,
                 progress: asyncio.Future, reps=1, addtitonal_info=None):
        self.exercise_func = exercise_func
        self.scheduled_time = scheduled_time
        self.notifier = notifier
        self.progress = progress
        self.reps = 1

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
        for _ in range(self.reps):
            for hand in ["Right", "Left"]:
                self.exercise_func(hand)
        self.progress.set_result(0)

if __name__ == '__main__':
    ex = ScheduledExercise(exercise4a, datetime.datetime.now()+datetime.timedelta(seconds=2), DesktopNotifier(), asyncio.Future())
    loop = asyncio.get_event_loop()
    loop.create_task(ex.notify())
    loop.run_until_complete(ex.progress)
