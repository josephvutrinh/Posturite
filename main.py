import cv2
import mediapipe as mp
import math
import collections

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize history for multiple landmarks
history = {
    'left_shoulder': collections.deque(maxlen=10),
    'right_shoulder': collections.deque(maxlen=10),
    'left_hip': collections.deque(maxlen=10),
    'right_hip': collections.deque(maxlen=10),
    'nose': collections.deque(maxlen=10),
}


def calculate_angle_3d(a, b, c):
    """Calculates the angle in 3D space between three points."""
    vec_ab = [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
    vec_cb = [c[0] - b[0], c[1] - b[1], c[2] - b[2]]

    dot_product = sum(va * vb for va, vb in zip(vec_ab, vec_cb))
    mag_ab = math.sqrt(sum(va ** 2 for va in vec_ab))
    mag_cb = math.sqrt(sum(vc ** 2 for vc in vec_cb))

    if mag_ab * mag_cb == 0:
        return 0  # Prevent division by zero

    angle = math.acos(dot_product / (mag_ab * mag_cb))
    return math.degrees(angle)


def smooth_landmark(landmark, history_queue):
    """Applies a moving average filter to a landmark coordinate."""
    history_queue.append((landmark.x, landmark.y))
    x_values, y_values = zip(*history_queue)
    return sum(x_values) / len(x_values), sum(y_values) / len(y_values)


def exponential_smoothing(new_value, prev_value, alpha=0.2):
    return alpha * new_value + (1 - alpha) * prev_value


def analyze_posture(landmarks):
    """Analyzes posture and provides feedback."""
    left_shoulder = [landmarks[11].x, landmarks[11].y, landmarks[11].z]
    right_shoulder = [landmarks[12].x, landmarks[12].y, landmarks[12].z]
    left_hip = [landmarks[23].x, landmarks[23].y, landmarks[23].z]
    right_hip = [landmarks[24].x, landmarks[24].y, landmarks[24].z]

    shoulder_angle_left = calculate_angle_3d(left_hip, left_shoulder, right_shoulder)
    shoulder_angle_right = calculate_angle_3d(right_hip, right_shoulder, left_shoulder)

    feedback = ""
    if shoulder_angle_left < 160 or shoulder_angle_right < 160:
        feedback += "Try to straighten your back and pull your shoulders back.\n"

    nose = [landmarks[0].x, landmarks[0].y, landmarks[0].z]
    mid_shoulder_x = (left_shoulder[0] + right_shoulder[0]) / 2
    if nose[0] < mid_shoulder_x - 0.05:
        feedback += "Your head is too far forward. Pull it back.\n"

    return feedback if feedback else "Posture looks good!"


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:
    try:
        prev_x, prev_y = 0, 0  # Initialize for smoothing

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                height, width, _ = image.shape

                for key in history.keys():
                    index = {'left_shoulder': 11, 'right_shoulder': 12, 'left_hip': 23, 'right_hip': 24, 'nose': 0}[key]
                    if landmarks[index].visibility > 0.6:  # Only process if visible
                        smoothed_x, smoothed_y = smooth_landmark(landmarks[index], history[key])
                        smoothed_x = exponential_smoothing(smoothed_x, prev_x)
                        smoothed_y = exponential_smoothing(smoothed_y, prev_y)
                        prev_x, prev_y = smoothed_x, smoothed_y

                feedback = analyze_posture(landmarks)
                cv2.putText(image, feedback, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                )

            cv2.imshow('MediaPipe Pose', image)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        cap.release()
        cv2.destroyAllWindows()
