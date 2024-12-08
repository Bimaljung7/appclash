import cv2
import mediapipe as mp
import time
import controller as cnt
time.sleep(2.0)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

tipid = [4, 8, 12, 16, 20]  # IDs of fingertip landmarks

video = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

    while True:
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmlist = []
        
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmlist.append([id, cx, cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hands.HAND_CONNECTIONS)

        finger = []
        if len(lmlist) != 0:
            # Thumb
            if lmlist[tipid[0]][1] > lmlist[tipid[0] - 1][1]:
                finger.append(1)
            else:
                finger.append(0)

            # Other finger
            for id in range(1, 5):
                if lmlist[tipid[id]][2] < lmlist[tipid[id] - 2][2]:
                    finger.append(1)
                else:
                    finger.append(0)

        total = finger.count(1)
        cnt.led(total)
        # Display the count for 0 and 5 fingers
        if total == 0:
            cv2.putText(image, "0", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
        elif total == 1:
            cv2.putText(image, "1", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
        elif total == 2:
            cv2.putText(image, "2", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
        elif total == 3:
            cv2.putText(image, "3", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
        elif total == 4:
            cv2.putText(image, "4", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
        elif total == 5:
            cv2.putText(image, "5", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)

        cv2.imshow("frame", image)
        k = cv2.waitKey(1)
        if k == ord("q"):
            break

video.release()
cv2.destroyAllWindows()
