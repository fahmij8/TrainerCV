# =========== Module 1, Step 3 : Model Testing =========== #
import cv2, json, sys
import tensorflow as tf
import numpy as np
sys.path.append("/usr/grading")
import grad
from PIL import Image

# Read Credential
f = open("trainer-userdata.json")
data = json.load(f)
usermail = data["email"]
flagGrading = False

# Load Models
model = tf.keras.models.load_model('model_module-1.h5')

# Load HAAR face classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load functions
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

# Initialize Webcam
print("[!] Initializing webcam") 

############# EDIT HERE!
cap = cv2.VideoCapture("#EDIT HERE#") # CHANGE WITH YOUR CAM URL
############# 

# Start Testing Model
while True:
    _, frame = video_capture.read()
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
            if(flagGrading == False):
                grad.doGrade(usermail, 1, 3)
                flagGrading = True
        # If prediction confidence < 0.5 your face is not detected
        else:
            cv2.putText(frame,"Empty", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2) #PUT YOUR NAME HERE
    # Else, webcam not detecting any images
    else:
        cv2.putText(frame,"No face found", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
    
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
