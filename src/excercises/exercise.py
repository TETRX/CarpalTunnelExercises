import cv2
import mediapipe as mp

from src.excercises.instruction_display import InstructionDisplay
from src.excercises.step_verification_result import StepVerificationResult


class Exercise:
    def __init__(self, steps, instruction_display: InstructionDisplay):
        self.steps = steps
        self.instruction_display = instruction_display
        self.current_step = 0

    def verify(self, hands):  # returns if we should continue running the exercise
        starting_step = self.current_step
        result = self.steps[self.current_step].verify(hands)
        while result == StepVerificationResult.SUCCESS:
            self.current_step += 1
            if self.current_step >= len(self.steps):
                self.instruction_display.display_success()
                return False
            result = self.steps[self.current_step].verify(hands)
        while result == StepVerificationResult.FAILURE:
            self.current_step -= 1
            result = self.steps[self.current_step].verify(hands)
        if starting_step != self.current_step:
            self.instruction_display.display_instruction(self.steps[self.current_step].instruction)
        return True

    def run(self):  # essentially just the sample code from google
        self.instruction_display.display_instruction(self.steps[self.current_step].instruction)

        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_hands = mp.solutions.hands

        # For webcam input:
        cap = cv2.VideoCapture(0)

        exercise_uncompleted = True
        with mp_hands.Hands(
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
            while cap.isOpened() and exercise_uncompleted:
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.flip(image, 1)

                results = hands.process(image)

                exercise_uncompleted = self.verify(results)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())

                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        cap.release()
