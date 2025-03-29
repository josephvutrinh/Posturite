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
        results = self.pose.process(imgRGB)

        if results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,
                                      results.pose_landmarks,
                                      self.mpPose.POSE_CONNECTIONS)
        return img

            # for id, lm in enumerate(results.pose_landmarks.landmark):
            #     h, w, c = img.shape
            #     print(id, lm)
            #     cx, cy = int(lm.x * w), int(lm.y * h)
            #     cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

def main():
    cap = cv2.VideoCapture(0)
    detector = PostureDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img)

        cv2.imshow("Live Camera", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()