import cv2

from src.excercises.exercise import Exercise
from src.excercises.hand_analysis.compute_angle import Finger, Joint
from src.excercises.instruction import Instruction
from src.excercises.instruction_display import InstructionDisplay
from src.excercises.steps.angle_constraint import HandAngleConstraint
from src.excercises.steps.angle_constraint_hold_step import HandAngleConstraintHoldStep
from src.excercises.steps.angle_constraint_step import HandAngleConstraintStep
from src.excercises.steps.fake_step import FakeHandStep
from src.excercises.steps.hand_in_frame_step import HandInFrameStep
import mediapipe as mp

def main():
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_holistic = mp.solutions.holistic

        # For webcam input:
        cap = cv2.VideoCapture(0)

        exercise_uncompleted = True
        with mp_holistic.Holistic(
                model_complexity=2,
                min_detection_confidence=0.8,
                min_tracking_confidence=0.8,
                smooth_landmarks=True,
                smooth_segmentation=True) as pose:
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

                results = pose.process(image)
                print(results.__dict__)
                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        results.pose_landmarks,
                        mp_holistic.POSE_CONNECTIONS,
                        mp_drawing_styles.get_default_pose_landmarks_style())
                for hand_landmarks in (results.left_hand_landmarks, results.right_hand_landmarks):
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_holistic.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style(),
                    )

                cv2.imshow('MediaPipe Pose', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        cap.release()
    # non_thumb_fingers = [finger for finger in Finger if finger != Finger.THUMB]
    # ex4a_step2_constraints = []
    # for finger in non_thumb_fingers:
    #     ex4a_step2_constraints.append(
    #         AngleConstraint(130, finger, Joint.FIRST, False)
    #     )
    #     ex4a_step2_constraints.append(
    #         AngleConstraint(140, finger, Joint.SECOND, True)
    #     )
    #     ex4a_step2_constraints.append(
    #         AngleConstraint(160, finger, Joint.THIRD, True)
    #     )
    #
    # ex4a_step2 = AngleConstraintStep("Right", Instruction("Curl your fingers",None),
    #                                  ex4a_step2_constraints
    #                                  )
    # ex4a_step2_hold = AngleConstraintHoldStep("Right",  Instruction("Keep your fingers curled",None), 4,
    #                                           ex4a_step2_constraints
    #                                           )
    #
    # steps = [HandInFrameStep("Right"), ex4a_step2, ex4a_step2_hold]
    # instruction_display = InstructionDisplay()
    # exercise = Exercise(steps, instruction_display)
    #
    # exercise.run()


if __name__ == '__main__':
    main()
