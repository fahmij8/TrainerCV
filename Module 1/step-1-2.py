# =========== Module 1, Step 1 Continued : Dataset Taking =========== #
import cv2
import sys, os, shutil, time, json
sys.path.append("/usr/grading")
import grad
from threading import Thread

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
    flagGraded = None
    # Directory Initialization
    print("[!] Inititalizing Directory")
    if(os.path.exists("dataset/empty")) :
        shutil.rmtree("dataset/empty")
        os.makedirs("dataset/empty")
        print("[!] Old Directory deleted, creating a new one")
    else :
        os.makedirs("dataset/empty")
        print("[!] Creating new directory") 

    # Initialize Webcam
    print("[!] Initializing webcam") 

    ############# EDIT HERE!
    cap = ThreadedCamera("") # CHANGE WITH YOUR CAM URL
    ############# 

    count = 0
    time.sleep(3)

    # Collect 20 samples of your face from webcam input
    print("[!] Taking samples") 
    while True:
        try:
            frame = cap.show_frame()
            if frame is not None:
                empty = cv2.resize(frame, (400, 400))

                # Save file in specified directory with unique name
                file_name_path = './dataset/empty/' + str(count) + '.jpg'
                cv2.imwrite(file_name_path, empty)
                count += 1
                # Put count on images and display live count
                cv2.putText(empty, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                cv2.imshow('Dataset Taker', empty)
                time.sleep(0.3)
                if cv2.waitKey(1) == 13: #Break with CTRL + C or Finish take dataset with 20 sample
                    flagGraded = False
                    break
                elif count == 20:
                    grad.doGrade(usermail, 1, 1)
                    break
            else:
                print("[!] Change your webcam URL if you see this many times.")
        except:
            print("[!] Change your webcam URL if you see this many times.")
            pass

    cv2.destroyAllWindows()      
    print("[!] Collecting Samples Complete")
    if(flagGraded == False):
        print("[!] You're not graded due to an error. Finish your dataset taking.")