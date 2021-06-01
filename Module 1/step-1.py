# =========== Module 1, Step 1 : Dataset Taking =========== #
import cv2
import os, shutil, time

# Directory Initialization
print("[!] Inititalizing Directory")
if(os.path.exists("dataset/myface")) :
    shutil.rmtree("dataset")
    os.makedirs("dataset/myface")
    print("[!] Old Directory deleted, creating a new one")
else :
    os.makedirs("dataset/myface") 
    print("[!] Creating new directory") 


# Load HAAR face classifier
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load functions
def face_extractor(img):
    # Function detects faces and returns the cropped face
    # If no face detected, it returns nothing
    faces = face_classifier.detectMultiScale(img, 1.3, 5)
    if faces is ():
        return None
    
    # Crop all faces found
    for (x,y,w,h) in faces:
        x=x-10
        y=y-10
        cropped_face = img[y:y+h+50, x:x+w+50]

    return cropped_face

# Initialize Webcam
print("[!] Initializing webcam") 

############# EDIT HERE!
cap = cv2.VideoCapture("#EDIT HERE#") # CHANGE WITH YOUR CAM URL
############# 

count = 0
time.sleep(3)

# Collect 20 samples of your face from webcam input
print("[!] Taking samples") 
while True:
    ret, frame = cap.read()
    if face_extractor(frame) is not None:
        count += 1
        face = cv2.resize(face_extractor(frame), (400, 400))

        # Save file in specified directory with unique name
        file_name_path = './dataset/myface/' + str(count) + '.jpg'
        cv2.imwrite(file_name_path, face)

        # Put count on images and display live count
        cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
        cv2.imshow('Dataset Taker', face)
        
    else:
        print("Face not found")
        pass

    if cv2.waitKey(1) == 13 or count == 20: #Break with CTRL + C or Finish take dataset with 20 sample
        break
        
cap.release()
cv2.destroyAllWindows()      
print("[!] Collecting Samples Complete")
