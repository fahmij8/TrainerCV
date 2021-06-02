# =========== Module 1, Step 3 : Model Testing =========== #
import cv2, json, sys, time
import tensorflow as tf
import numpy as np
sys.path.append("/usr/grading")
import grad
from PIL import Image
from threading import Thread

# Face Extractor functions
def face_extractor(img):
    # Function detects faces and returns the cropped face
    # If no face detected, it returns nothing
    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    
    if faces is ():
        return None

    # Give bounding box to any detected face
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        cropped_face = img[y:y+h, x:x+w]

    return cropped_face

# Threading Capture
class ThreadedCamera(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.status = False
        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)

        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(self.FPS)

    def show_frame(self):
        if self.status:
            return self.frame
        return None 

if __name__ == '__main__':
    # Read Credential
    f = open("trainer-userdata.json")
    data = json.load(f)
    usermail = data["email"]

    # Load Models
    model = tf.keras.models.load_model('model_module-1.h5')

    # Load HAAR face classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Initialize Webcam
    print("[!] Initializing webcam") 

    ############# EDIT HERE!
    cap = ThreadedCamera("") # CHANGE WITH YOUR CAM URL
    ############# 

    # Testing Model
    while True:
        try:
            frame = cap.show_frame()
            face=face_extractor(frame)
            # If Webcam detecting face
            if type(face) is np.ndarray:
                # Preprocess Image
                face = cv2.resize(face, (224, 224))
                im = Image.fromarray(face, 'RGB')
                img_array = np.array(im)
                img_array = np.expand_dims(img_array, axis=0)
                pred = model.predict(img_array)

                # Image Labeling
                # If prediction confidence > 0.5 your face is detected  
                if(pred[0][0]>0.5):
                    ############# EDIT HERE!
                    cv2.putText(frame,"#EDIT HERE#", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2) #PUT YOUR NAME HERE
                    #############
                    flagGrading = False
            # Else, webcam not detecting any images
            else:
                cv2.putText(frame,"Empty", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
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
    if(flagGrading == False):
        grad.doGrade(usermail, 1, 3)
    else:
        print("[!] You're not graded due to an error")