import cv2
import mediapipe as mp
import servo as se

mp_hands=mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils

def map_coord_angle(value,max_value):
    return int((value/max_value)*180)

cap=cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        sucess,image=cap.read()
        if not sucess:
            break

        image_rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        results=hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                mp_drawing.draw_landmarks(image,hand_landmarks,mp_hands.HAND_CONNECTIONS)

            #Extracting hand landmarks

            h,w,c=image.shape
            index_finger=hand_landmarks.landmark[8]
            # for id, lm in enumerate(hand_landmarks.landmark):
            cx,cy= int (index_finger.x*w), int(index_finger.y*h)

            angle_x=map_coord_angle(cx,w)
            angle_y=map_coord_angle(cy,h)

            se.get_angle(angle_x,angle_y)

            cv2.circle(image,(cx,cy),5,(255,0,0),-5)

            # x_min = min(int(lm.x * w))
            # y_min = min([int(lm.y * h) for lm in hand_landmarks.landmark])
            # x_max = max([int(lm.x * w) for lm in hand_landmarks.landmark])
            # y_max = max([int(lm.y * h) for lm in hand_landmarks.landmark])  
            cv2.putText(image,f"x:{angle_x},y:{angle_y}",(45,375),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) 
            cv2.putText(image, f"Index Tip: ({cx}, {cy})", (cx + 20, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # cv2.putText(image, f'x:{x_max}', (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
            # cv2.putText(image, f'y:{y_max}', (45, 4), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow("learning",image)
        k= cv2.waitKey(1)
        if k==ord("q"):
         break

cap.release()
cv2.destroyAllWindows()
