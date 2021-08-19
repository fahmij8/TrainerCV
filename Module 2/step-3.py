# =========== Module 2, Step 3 : Model Testing =========== #
import cv2, sys
import tensorflow as tf
import numpy as np
import utilities_modul as util
sys.path.append("/usr/grading")
import grad
from PIL import Image

if __name__ == '__main__':
    # Read Credential
    usermail = util.init_data("email")

    # Load Models
    model = tf.keras.models.load_model('model_module-2.h5')

    # Load HAAR face classifier
    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Initialize Webcam
    cap = util.init_camera(util.init_data("urlCamera"))
    detectedTimes = 15 #EDIT THIS IF YOU WANT TO DETECT MORE LONGER
    flagGrading = False

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
                    detectedTimes -= 1 
                    label = f"First Face : ({confidence}%)"
                    cv2.putText(frame,label, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                elif(result == 2):
                    detectedTimes -= 1
                    label = f"Second Face : ({confidence}%)"
                    cv2.putText(frame,label, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                else:
                    label = f"Emtpy : ({confidence}%)"
                    cv2.putText(frame,label, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 2)

                if(detectedTimes == 0 and flagGrading == False):
                    cv2.destroyAllWindows()
                    grad.doGrade(usermail, 2, 3)
                    break
            # Else, webcam not detecting any images
            else:
                cv2.putText(frame,"Empty", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
                flagGrading = False
            
            cv2.imshow('Video', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            flagGrading = None
            print("[!] Change your webcam URL if you see this many times.")
            pass

    cv2.destroyAllWindows()
    print("[!] Testing Model Complete")