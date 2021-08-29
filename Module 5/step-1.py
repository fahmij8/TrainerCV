# =========== Module 5, Step 1 : Getting started with mediapipe =========== #
import cv2, mediapipe, traceback
import utilities_modul as util

if __name__ == '__main__':
    # Clear memory
    util.init_clearmemory()

    # Read Credential
    usermail = util.init_data("email")
    
    # Initialize mediapipe library
    medhands=mediapipe.solutions.hands
    hands=medhands.Hands(max_num_hands=1,min_detection_confidence=0.7)
    draw=mediapipe.solutions.drawing_utils
    #styles = mediapipe.solutions.drawing_styles

    # Initialize webcam
    cap = util.init_camera(util.init_data("urlCamera"))
    detectedTimes = 0

    while True:
        try:
            success, img=cap.read()
            img = cv2.flip(img,1)
            imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
            res = hands.process(imgrgb)
            
            if res.multi_hand_landmarks:
                for hand_landmarks in res.multi_hand_landmarks:
                    detectedTimes += 1
                    draw.draw_landmarks(img,
                                        hand_landmarks,
                                        util.hand_connections(),
                                        draw.DrawingSpec(color=(0,0,0),thickness=2,circle_radius=3),
                                        draw.DrawingSpec(color=(0,255,255),thickness=2,circle_radius=3))

                    for idx,lm in enumerate(hand_landmarks.landmark):
                        if(idx == 8):
                            h,w,c= img.shape
                            cx,cy=int(lm.x * w) , int(lm.y * h)
                            cv2.circle(img, (cx,cy), 7, (255,0,0), 10)

            cv2.imshow("hand gestures",img)
            
            #press q to quit
            if cv2.waitKey(1) == ord('q'):
                util.give_grading(usermail=usermail, steps=1, optionalParam=detectedTimes)
                break

        except:
            print("Unexpected error:", traceback.format_exc())
            break

    print("[!] Testing mediapipe hands completed!")
    cv2.destroyAllWindows()