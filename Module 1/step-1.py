# =========== Module 1, Step 1 : Dataset Taking (Your Face Sample) =========== #
import cv2
import os, shutil, time
from threading import Thread

# Face Extractor functions
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

    # Initialize Webcam
    print("[!] Initializing webcam") 

    ############# EDIT HERE!
    cap = ThreadedCamera("") # CHANGE WITH YOUR CAM URL
    ############# 

    count = 0

    # Collect 20 samples of your face from webcam input
    print("[!] Taking samples") 
    while True:
        try:
            frame = cap.show_frame()
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
        except:
            print("[!] Change your webcam URL if you see this many times.")
            pass    

    cv2.destroyAllWindows()      
    print("[!] Collecting Samples Complete")