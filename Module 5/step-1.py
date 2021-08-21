# =========== Module 5, Step 1 : Getting started with mediapipe =========== #
import cv2
import mediapipe
import utilities_modul as util

if __name__ == '__main__':
    # Read Credential
    usermail = util.init_data("email")
    
    # Initialize mediapipe library
    medhands=mediapipe.solutions.hands
    hands=medhands.Hands(max_num_hands=1,min_detection_confidence=0.7)
    draw=mediapipe.solutions.drawing_utils
    styles = mediapipe.solutions.drawing_styles

    # Initialize webcam
    cap = util.init_camera(util.init_data("urlCamera"))
    detectedTimes = 0

    while True:
        success, img=cap.read()
        img = cv2.flip(img,1)
        imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
        res = hands.process(imgrgb)
        
        if res.multi_hand_landmarks:
            for hand_landmarks in res.multi_hand_landmarks:
                detectedTimes += 1
                draw.draw_landmarks(img,
                                    hand_landmarks,
                                    medhands.HAND_CONNECTIONS,
                                    util.landmark_style_index(),
                                    draw.DrawingSpec(color=(0,255,0),thickness=2,circle_radius=3))

        cv2.imshow("hand gestures",img)
        
        #press q to quit
        if cv2.waitKey(1) == ord('q'):
            util.give_grading(usermail=usermail, steps=1, optionalParam=detectedTimes)
            break
        
    cv2.destroyAllWindows()