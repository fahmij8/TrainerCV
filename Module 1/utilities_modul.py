import cv2
import os, shutil, json, requests, sys
sys.path.append("/usr/grading")
import grad

# Take user data function
def init_data(types):
    f = open("trainer-userdata.json")
    data = json.load(f)
    return data[types]
    

# Face Extractor function
def face_extractor(img, face_classifier):
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

# Face Extractor functions
def face_extractor_boundaries(img, face_classifier):
    # Function detects faces and returns the cropped face
    # If no face detected, it returns nothing
    faces = face_classifier.detectMultiScale(img, 1.3, 5)
    if faces is ():
        return img

    # Give bounding box to any detected face
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        cropped_face = img[y:y+h, x:x+w]

    return cropped_face

#Initialize Directory Function
def init_directory(mode):
    if(mode == 1):
        print("[!] Inititalizing Directory")
        if(os.path.exists("dataset/myface")) :
            shutil.rmtree("dataset")
            os.makedirs("dataset/myface")
            print("[!] Old Directory deleted, creating a new one")
        else :
            os.makedirs("dataset/myface") 
            print("[!] Creating new directory")
    elif(mode == 2):
        print("[!] Inititalizing Directory")
        if(os.path.exists("dataset/empty")) :
            shutil.rmtree("dataset/empty")
            os.makedirs("dataset/empty")
            print("[!] Old Directory deleted, creating a new one")
        else :
            os.makedirs("dataset/empty")
            print("[!] Creating new directory")

# Initialize Camera Function
def init_camera(url):
    print("[!] Initializing webcam") 
    cap = cv2.VideoCapture(url) # CHANGE WITH YOUR CAM URL
    return cap 

# Post LED State Function
def postRequest(predict, appname, devicename, key):
    # Function to push state of LED to antares devices
    url = "https://platform.antares.id:8443/~/antares-cse/antares-id/" + appname + "/" + devicename
    payload = "{\r\n    \"m2m:cin\": {\r\n    \"con\": \"{\\\"led\\\":" + str(predict) + "}\"\r\n    }\r\n}"
    headers = {
    'x-m2m-origin': key,
    'content-type': "application/json;ty=4",
    'accept': "application/json",
    'cache-control': "no-cache",
    'postman-token': "e10b0cdc-98bc-4459-be34-25417d5f57bd"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response

def give_grading(usermail, steps):
    steps = int(steps)
    status = grad.doGrade(usermail, 1, steps)
    return status