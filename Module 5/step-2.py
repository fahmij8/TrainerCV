# =========== Module 5, Step 2 : Detecting tip of index finger using mediapipe =========== #
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
    
    while True:
        success, img=cap.read()
        img = cv2.flip(img,1)
        image_height, image_width, _ = img.shape
        imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
        res = hands.process(imgrgb)
        
        lmlist=[]
        tipids=[4,8,12,16,20] #list of all landmarks of the tips of fingers
        
        cv2.rectangle(img,(20,400),(460,440),(0,255,204),cv2.FILLED)
        cv2.rectangle(img,(20,400),(460,440),(0,0,0),5)
        
        if res.multi_hand_landmarks:
            for hand_landmarks in res.multi_hand_landmarks:
                for idx,lm in enumerate(hand_landmarks.landmark):
                    h,w,c= img.shape
                    cx,cy=int(lm.x * w) , int(lm.y * h)
                    lmlist.append([idx,cx,cy])
                    if len(lmlist) != 0 and len(lmlist)==21:
                        # Try to inspect variable lmlist first!
                        # Detailed hand landmark key : https://google.github.io/mediapipe/images/mobile/hand_landmarks.png
                        if(lmlist[8][2] < lmlist[5][2]):
                            result = "Index finger tip is raised"
                        else :
                            result = "Index finger tip is closed"
                        cv2.putText(img,result,(25,430),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),1)
                        
                    #change color of points and lines
                    draw.draw_landmarks(img,
                                        hand_landmarks,
                                        medhands.HAND_CONNECTIONS,
                                        util.landmark_style_index(),
                                        draw.DrawingSpec(color=(0,255,0),thickness=2,circle_radius=3))

        cv2.imshow("hand gestures",img)
        
        #press q to quit
        if cv2.waitKey(1) == ord('q'):
            break
        
    cv2.destroyAllWindows()