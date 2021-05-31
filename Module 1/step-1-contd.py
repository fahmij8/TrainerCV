import cv2
import os, shutil, time

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
cap = cv2.VideoCapture("http://camera-cv-web.herokuapp.com/video_feed") #EDIT HERE!
count = 0
time.sleep(3)

# Collect 100 samples of your face from webcam input
print("[!] Taking samples") 
while True:
    ret, frame = cap.read()
    count += 1
    face = cv2.resize(frame, (400, 400))

    # Save file in specified directory with unique name
    file_name_path = './dataset/empty/' + str(count) + '.jpg'
    cv2.imwrite(file_name_path, face)

    # Put count on images and display live count
    cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
    cv2.imshow('Dataset Taker', face)


    if cv2.waitKey(1) == 13 or count == 20: #13 is the Enter Key
        break
        
cap.release()
cv2.destroyAllWindows()      
print("[!] Collecting Samples Complete")