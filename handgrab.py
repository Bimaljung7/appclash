import mediapipe as mp
import cv2

# Initialize Mediapipe hands and drawing utils
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Fingertip IDs for detection
tip_ids = [4, 8, 12, 16, 20]

# Capture video from webcam
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Convert image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = hands.process(image_rgb)

        # Flip image for mirror effect
        image = cv2.flip(image, 1)
        h, w, c = image.shape  # Get image dimensions
        lmlist = []

        # If hand landmarks detected
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Collect landmark positions
                for id, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmlist.append([id, cx, cy])

                # Draw hand landmarks
                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Check finger status if landmarks exist
        if lmlist:
            fingers_open = []
            # Thumb: Compare x-coordinates instead of y
            if lmlist[tip_ids[0]][1] > lmlist[tip_ids[0] - 1][1]:  # Thumb open logic
                fingers_open.append(True)
            else:
                fingers_open.append(False)

            # Other fingers
            for id in range(1, 5):
                if lmlist[tip_ids[id]][2] < lmlist[tip_ids[id] - 2][2]:  # Open if tip above dip
                    fingers_open.append(True)
                else:
                    fingers_open.append(False)

            # Display status on screen
            status_text = f"Fingers Open: {fingers_open.count(True)}"
            cv2.putText(image, status_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the image
        cv2.imshow("Hand Tracking", image)

        # Exit loop on 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
