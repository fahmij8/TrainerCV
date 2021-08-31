# =========== Module 2, Step 4 : Model Testing (IoT Implementation) =========== #
import cv2, traceback
import tensorflow as tf
import numpy as np
import utilities_modul as util
from PIL import Image

if __name__ == '__main__':
    # Clear memory
    util.init_clearmemory()
    
    # Read Credential
    usermail = util.init_data("email")
    appName = util.init_data("appName")
    deviceName = util.init_data("deviceName")
    key = util.init_data("xm2morigin")

    # Load Models
    model = tf.keras.models.load_model('model_module-2.h5')

    # Load HAAR face classifier
    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Initialize Webcam
    cap = util.init_camera(util.init_data("urlCamera"))
    detectedTimes = 0

    # Testing Model
    while True:
        try:
            ret, frame = cap.read()
            face=util.face_extractor_boundaries(frame, face_classifier)
            # If Webcam detecting face
            if type(face) is np.ndarray:
                # Preprocess Image
                face = cv2.resize(face, (224, 224))
                im = Image.fromarray(face, 'RGB')
                img_array = np.array(im)
                img_array = np.expand_dims(img_array, axis=0)
                pred = model.predict(img_array)
                result = np.argmax(pred)
                confidence = int(pred[0][result] * 100)
                
                # Image Labeling
                # If prediction confidence > 0.5 your face is detected 
                if(result == 1):
                    detectedTimes += 1 
                    label = f"First Face : ({confidence}%)"
                    cv2.putText(frame,label, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                    util.postRequest(1, appName, deviceName, key)
                elif(result == 2):
                    detectedTimes += 1
                    label = f"Second Face : ({confidence}%)"
                    cv2.putText(frame,label, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                    util.postRequest(2, appName, deviceName, key)
                else:
                    label = f"Emtpy : ({confidence}%)"
                    cv2.putText(frame,label, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 2)
                    util.postRequest(0, appName, deviceName, key)
                print(f'{detectedTimes} => {pred}')
                
            # Else, webcam not detecting any images
            else:
                cv2.putText(frame,"Empty", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
            
            cv2.imshow('Video', frame)
            
            # To quit press q in OpenCV window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                util.give_grading(usermail=usermail, steps=4, optionalParam=detectedTimes)
                break
            
        except:
            print("Unexpected error:", traceback.format_exc())
            break

    cv2.destroyAllWindows()
    print("[!] Testing Model Complete")