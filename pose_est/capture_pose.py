import os
import cv2
import mediapipe as mp
import pandas as pd

# import numpy as np
op_path = '../output/'


def start_capture(path=0, save_output=False):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(path)

    pose_at_frame = []
    calc_timestamps = []
    offset = 0.0
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            flag, frame = cap.read()

            if flag:
                if len(calc_timestamps) == 0:
                    offset = cap.get(cv2.CAP_PROP_POS_MSEC)
                    calc_timestamps.append(0.0)
                else:
                    calc_timestamps.append(calc_timestamps[-1] + cap.get(cv2.CAP_PROP_POS_MSEC) - offset)

                # detect and render
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # print("image", type(image))

                # make detection
                results = pose.process(image)

                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                landmarks = []
                for landmark in results.pose_landmarks.landmark:
                    landmarks.append({
                        'X': landmark.x,
                        'Y': landmark.y,
                        'Z': landmark.z,
                        'Visibility': landmark.visibility,
                    })
                pose_at_frame.append({
                    'timestamp': calc_timestamps[-1],
                    'landmarks': landmarks,
                })

                # render detections
                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
                )

                # show the detected poses
                cv2.imshow("Mediapipe feed", image)
            else:
                break

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
    df = pd.DataFrame(pose_at_frame)
    if save_output:
        path = os.path.join(op_path, 'output.csv')
        df.to_csv(path)

    cap.release()
    cv2.destroyAllWindows()
