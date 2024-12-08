import cv2
import mediapipe as mp

#initialize diffrent function of the above modules
mp_hands= mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils

#capturing video
cap=cv2.VideoCapture(0) # 0 for default camera

with mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.7) as hands:
# the above block initializes the functions of mediapipe hand module and assigs it to hands so that we can do things like getting hand landmarks 

    # aaba loop chalauneee
    while cap.isOpened():
        sucess,image=cap.read()
        if not sucess:
            break

        image_rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB) # open cv le input bgr form ma linxa meaning in order blue green red
                                                        # but mediapipe takes or process the data in rgb form
        result=hands.process(image_rgb)

        if result.multi_hand_landmarks:
            for hand_landmark in result.multi_hand_landmarks:

                mp_drawing.draw_landmarks(image,hand_landmark,mp_hands.HAND_CONNECTION)

                # aaba hand landmark lai aafno aawaskta aanusar extract garnee
                h,w,c=image.shape()
                index_finger=hand_landmark.landmark[7]

                cx,cy=int (index_finger.x*w), int(index_finger.y*h)
                # in the above line the pixels are converted to coordinate ranging from 0 to 180 in both axes
                

        
               

