# =========== Module 5, Step 4 : IoT Implementation with mediapipe =========== #
import cv2, mediapipe, traceback
import utilities_modul as util

if __name__ == '__main__':
    # Clear memory
    util.init_clearmemory()

    # Read Credential
    usermail = util.init_data("email")
    appName = util.init_data("appName")
    deviceName = util.init_data("deviceName")
    key = util.init_data("xm2morigin")

    # Initialize mediapipe library
    medhands = mediapipe.solutions.hands
    hands = medhands.Hands(max_num_hands=1,min_detection_confidence=0.7)
    draw = mediapipe.solutions.drawing_utils

    # Initialize webcam
    cap = util.init_camera(util.init_data("urlCamera"))
    detectedTimes = 0

    while True:
        try:
            success, img=cap.read()
            img = cv2.flip(img,1)
            imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
            res = hands.process(imgrgb)
            lmlist = []
            tipids=[4,8,12,16,20] #list of all landmarks of the tips of fingers

            if res.multi_hand_landmarks:
                for hand_landmarks in res.multi_hand_landmarks:
                    for idx,lm in enumerate(hand_landmarks.landmark):
                        h,w,c= img.shape
                        cx,cy=int(lm.x * w) , int(lm.y * h)
                        lmlist.append([idx,cx,cy])

                        if len(lmlist) != 0 and len(lmlist)==21:
                            detectedTimes += 1
                            # TODO : Create your own logic to determine number from hand gesture
                            # Store the result on `result` variable
                            # Detailed hand landmark key : https://google.github.io/mediapipe/images/mobile/hand_landmarks.png
                            result = util.show_answer_step_3(lmlist, tipids)

                            print(f'{detectedTimes} => {result}')
                            cv2.rectangle(img,(20,400),(50,440),(0,255,204),cv2.FILLED)
                            cv2.rectangle(img,(20,400),(50,440),(0,0,0),5)
                            cv2.putText(img,str(result['fingerCount']),(25,430),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
                            util.postRequest(str(result['fingerCount']), appName, deviceName, key)

                        draw.draw_landmarks(img,
                                            hand_landmarks,
                                            util.hand_connections(),
                                            draw.DrawingSpec(color=(0,0,0),thickness=2,circle_radius=3),
                                            draw.DrawingSpec(color=(0,255,255),thickness=2,circle_radius=3))

            cv2.imshow("hand gestures",img)
            
            #press q to quit
            if cv2.waitKey(1) == ord('q'):
                if('useHelp' in result):
                    util.give_grading(usermail=usermail, steps=4, optionalParam=[True, detectedTimes])
                else:
                    util.give_grading(usermail=usermail, steps=4, optionalParam=[False, detectedTimes])
                break

        except:
            print("Unexpected error:", traceback.format_exc())
            break

    print("[!] Testing mediapipe hands completed!")
    cv2.destroyAllWindows()