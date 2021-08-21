# =========== Module 1, Step 3 : Model Testing =========== #
import cv2, sys
import tensorflow as tf
import numpy as np
import utilities_modul as util
from PIL import Image

if __name__ == '__main__':
    # Read Credential
    usermail = util.init_data("email")

    # Load Models
    model = tf.keras.models.load_model('model_module-1.h5')

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
                confidence = int(pred[0][0] * 100)
                print(f'{detectedTimes} => {pred}')
                # Image Labeling
                # If prediction confidence > 0.5 your face is detected 
                if(confidence > 50):
                    detectedTimes += 1 
                    label = f"Face : ({confidence}%)"
                    cv2.putText(frame,label, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                else:
                    label = f"Emtpy : ({confidence}%)"
                    cv2.putText(frame,label, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 2)
            # Else, webcam not detecting any images
            else:
                cv2.putText(frame,"Empty", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            
            cv2.imshow('Video', frame)
            
            # To quit press q in OpenCV window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                util.give_grading(usermail=usermail, steps=3, optionalParam=detectedTimes)
                break
        except:
            print("Unexpected error:", sys.exc_info())
            break

    cv2.destroyAllWindows()
    print("[!] Testing Model Complete")