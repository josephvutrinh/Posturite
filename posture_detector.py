import cv2
import mediapipe as mp


class PostureDetector:
    def __init__(self,
                 mode = False,
                 upBody = False,
                 smooth = True,
                 detectCon = 0.5,
                 trackCon = 0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectCon = detectCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode = self.mode,
                                     model_complexity = 1,
                                     smooth_landmarks = self.smooth,
                                     min_detection_confidence = self.detectCon,
                                     min_tracking_confidence = self.trackCon)

    def findPose(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,
                                      self.results.pose_landmarks,
                                      self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw = True):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                cz = int(lm.z)
                lmList.append([id, cy, cz,])
                if draw:
                   cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        return lmList

    def detectForwardHead(self, lmList, threshold = 0.1):
        if lmList:
            nose_z = lmList[0][2]
            left_shoulder_z = lmList[11][2]
            right_shoulder_z = lmList[12][2]

            shoulder_z_avg = (left_shoulder_z + right_shoulder_z) / 2

            if nose_z < shoulder_z_avg - threshold * abs(shoulder_z_avg):
                return True
        return False

    def detectedShruggedShoulder(self, lmList, threshold = 0.287):
        if lmList:
            left_mouth_y = lmList[9][1]
            right_mouth_y = lmList[10][1]
            left_shoulder_y = lmList[11][1]
            right_shoulder_y = lmList[12][1]

            if left_mouth_y < left_shoulder_y - (threshold * 1.2) * abs(
                left_shoulder_y) and right_mouth_y < right_shoulder_y - (threshold * 1.2) * abs(right_shoulder_y):                return True
        return False


def main():
    cap = cv2.VideoCapture(0)
    detector = PostureDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img)
        print(lmList)

        if detector.detectForwardHead(lmList) and detector.detectedShruggedShoulder(lmList):
            cv2.putText(img, "Forward Head and Shrugged Shoulders Detected!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            print("⚠️Forward Head and Shrugged Shoulders Detected!")

        elif detector.detectedShruggedShoulder(lmList):
            cv2.putText(img, "Shrugged Shoulder Detected!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            print("⚠️Shrugged Shoulder Detected!")

        elif detector.detectForwardHead(lmList):
            cv2.putText(img, "Forward Head Detected!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            print("⚠️Forward Head Detected!")


        if not detector.detectForwardHead(lmList) and not detector.detectedShruggedShoulder(lmList) :
            cv2.putText(img, "Good Posture", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            print("Good")

        cv2.imshow("Live Camera", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()