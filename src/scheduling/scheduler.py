import asyncio
import datetime
import json
import os
from asyncio import Future
from threading import Thread

import pause
from desktop_notifier import DesktopNotifier

from src.excercises.excercises.exercise1 import exercise1
from src.excercises.excercises.exercise3 import exercise3
from src.excercises.excercises.exercise4a import exercise4a
from src.excercises.excercises.exercise4b import exercise4b
from src.excercises.instruction_display import TKInstructionDisplay, SimpleInstructionDisplay
from src.img.img_process import get_img
from src.scheduling.scheduled_exercise import ScheduledExercise


class Scheduler:
    code_to_func = {
        "1": exercise1,
        "3": exercise3,
        "4a": exercise4a,
        "4b": exercise4b
    }

    def __init__(self, notifier: DesktopNotifier, instruction_display, path: str="../schedule.json"):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.exercises = []
        self.notifier = notifier
        self.path = path
        self.instruction_display = instruction_display
        self.load()

    def load(self):
        with open(self.path, "r") as f:
            schedule_dict = json.load(f)

        today = datetime.datetime.now().date()
        today = datetime.datetime.combine(today, datetime.datetime.min.time())
        for exercise, details in schedule_dict.items():
            for time in details["schedule"]:
                next_time = today + datetime.timedelta(hours=time["hour"], minutes=time["minute"])
                if next_time < datetime.datetime.now():  # if todays time passed, schedule the same day tommorow
                    next_time += datetime.timedelta(days=1)
                new_future = Future()
                self.exercises.append(ScheduledExercise(Scheduler.code_to_func[exercise], next_time, self.notifier,
                                                        new_future, self.instruction_display, reps=details["reps"],
                                                        addtitonal_info=None if "additional_info" not in details else details["additional_info"]))
        self.exercises.sort(key=lambda x: x.scheduled_time)
        for ex in self.exercises:
            print(ex.scheduled_time)

    def await_next_ex(self):
        pause.until(self.exercises[0].scheduled_time)
        current_exercise = self.exercises[0]
        loop = asyncio.get_event_loop()
        loop.create_task(current_exercise.notify())
        loop.run_until_complete(current_exercise.progress)

        next_day_exercise = ScheduledExercise(current_exercise.exercise_func,
                                              current_exercise.scheduled_time + datetime.timedelta(days=1),
                                              self.notifier,
                                              Future(),
                                              reps=current_exercise.reps,
                                              addtitonal_info=current_exercise.additional_info)
        self.exercises.pop()
        self.exercises.append(next_day_exercise)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.await_next_ex())
        loop.run_forever()


if __name__ == '__main__':
    success_image = get_img("../../img/success.png")
    instruction_display = TKInstructionDisplay(success_image=success_image)
    # instruction_display = SimpleInstructionDisplay()
    def schedule_task():
        scheduler = Scheduler(DesktopNotifier(), instruction_display, path="../../schedule.json")
        scheduler.run()

    thread = Thread(target=schedule_task)
    thread.start()

    instruction_display.run()









