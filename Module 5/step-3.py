# =========== Module 5, Step 3 : Creating logic to detect digit from hand gesture =========== #
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

    # Initialize webcam
    cap = util.init_camera(util.init_data("urlCamera"))
    useHelp = False
    
    while True:
        success, img=cap.read()
        img = cv2.flip(img,1)
        imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
        res = hands.process(imgrgb)
        
        lmlist=[]
        tipids=[4,8,12,16,20] #list of all landmarks of the tips of fingers
        
        cv2.rectangle(img,(20,350),(90,440),(0,255,204),cv2.FILLED)
        cv2.rectangle(img,(20,350),(90,440),(0,0,0),5)
        
        if res.multi_hand_landmarks:
            for hand_landmarks in res.multi_hand_landmarks:
                for idx,lm in enumerate(hand_landmarks.landmark):
                    h,w,c= img.shape
                    cx,cy=int(lm.x * w) , int(lm.y * h)
                    lmlist.append([idx,cx,cy])
                    # TODO : Create your own logic to detect number gesture as shown in step-2
                    # Comment lines 39-40 to use your own answer, store the logic to `result` variable
                    fingercount = util.show_answer_step_3(lmlist, tipids)
                    result = fingercount['fingerCount']
                    cv2.putText(img,str(result),(25,430),cv2.FONT_HERSHEY_PLAIN,6,(0,0,0),5)
                        
                    #change color of points and lines
                    draw.draw_landmarks(img,hand_landmarks,medhands.HAND_CONNECTIONS,draw.DrawingSpec(color=(0,255,204),thickness=2,circle_radius=2),draw.DrawingSpec(color=(0,0,0),thickness=2,circle_radius=3))

        cv2.imshow("hand gestures",img)
        
        #press q to quit
        if cv2.waitKey(1) == ord('q'):
            break
        
    cv2.destroyAllWindows()