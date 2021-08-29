import cv2
import os, shutil, json, requests, sys
from mediapipe.python.solutions.hands import HandLandmark

def init_clearmemory():
    os.system("free -h")
    os.system("echo 'upi123' | sudo -S -k sh -c 'echo 3 > /proc/sys/vm/drop_caches' ")
    os.system("free -h")

# Take user data function
def init_data(types):
    f = open("trainer-userdata.json")
    data = json.load(f)
    return data[types]
    

#Initialize Directory Function
def init_directory(mode):
    if(mode == 1):
        print("[!] Inititalizing Directory")
        if(os.path.exists("dataset")) :
            shutil.rmtree("dataset")
        

# Initialize Camera Function
def init_camera(url):
    print("[!] Initializing webcam") 
    cap = cv2.VideoCapture(url) # CHANGE WITH YOUR CAM URL
    return cap 

# Post LED State Function
def postRequest(predict, appname, devicename, key):
    # Function to push state of LED to antares devices
    url = "https://platform.antares.id:8443/~/antares-cse/antares-id/" + appname + "/" + devicename
    payload = "{\r\n    \"m2m:cin\": {\r\n    \"con\": \"{\\\"number\\\":" + str(predict) + "}\"\r\n    }\r\n}"
    headers = {
        'x-m2m-origin': key,
        'content-type': "application/json;ty=4",
        'accept': "application/json",
        'cache-control': "no-cache",
        'postman-token': "e10b0cdc-98bc-4459-be34-25417d5f57bd"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    if(response.status_code == 201):
        return response
    else:
        sys.exit()

def give_grading(usermail, steps, *args, **kwargs):
    optionalParam = kwargs.get('optionalParam')
    payload = json.dumps({
        "usermail": usermail,
        "steps": steps,
        "optionalParam": optionalParam
    })
    
    url = "https://trainercv-grading.herokuapp.com/grad-module-5"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    if(response.status_code == 200):
        print(json.loads(response.text)['message'])
    else:
        sys.exit()

def hand_connections():
    return frozenset([
        (HandLandmark.WRIST, HandLandmark.THUMB_CMC),
        (HandLandmark.THUMB_CMC, HandLandmark.THUMB_MCP),
        (HandLandmark.THUMB_MCP, HandLandmark.THUMB_IP),
        (HandLandmark.THUMB_IP, HandLandmark.THUMB_TIP),
        (HandLandmark.INDEX_FINGER_MCP, HandLandmark.INDEX_FINGER_PIP),
        (HandLandmark.INDEX_FINGER_PIP, HandLandmark.INDEX_FINGER_DIP),
        (HandLandmark.INDEX_FINGER_DIP, HandLandmark.INDEX_FINGER_TIP),
        (HandLandmark.INDEX_FINGER_MCP, HandLandmark.MIDDLE_FINGER_MCP),
        (HandLandmark.MIDDLE_FINGER_MCP, HandLandmark.MIDDLE_FINGER_PIP),
        (HandLandmark.MIDDLE_FINGER_PIP, HandLandmark.MIDDLE_FINGER_DIP),
        (HandLandmark.MIDDLE_FINGER_DIP, HandLandmark.MIDDLE_FINGER_TIP),
        (HandLandmark.MIDDLE_FINGER_MCP, HandLandmark.RING_FINGER_MCP),
        (HandLandmark.RING_FINGER_MCP, HandLandmark.RING_FINGER_PIP),
        (HandLandmark.RING_FINGER_PIP, HandLandmark.RING_FINGER_DIP),
        (HandLandmark.RING_FINGER_DIP, HandLandmark.RING_FINGER_TIP),
        (HandLandmark.RING_FINGER_MCP, HandLandmark.PINKY_MCP),
        (HandLandmark.WRIST, HandLandmark.PINKY_MCP),
        (HandLandmark.PINKY_MCP, HandLandmark.PINKY_PIP),
        (HandLandmark.PINKY_PIP, HandLandmark.PINKY_DIP),
        (HandLandmark.PINKY_DIP, HandLandmark.PINKY_TIP),
        (HandLandmark.INDEX_FINGER_MCP, HandLandmark.THUMB_CMC)
    ])


def show_answer_step_3(lmlist, tipids):
    result = dict();
    if len(lmlist) != 0 and len(lmlist)==21:
        fingerlist=[]
        #thumb and dealing with flipping of hands
        if lmlist[12][1] > lmlist[20][1]:
            if lmlist[tipids[0]][1] > lmlist[tipids[0]-1][1]:
                fingerlist.append(1)
            else:
                fingerlist.append(0)
        else:
            if lmlist[tipids[0]][1] < lmlist[tipids[0]-1][1]:
                fingerlist.append(1)
            else:
                fingerlist.append(0)
        
        #others
        for idx in range (1,5):
            if lmlist[tipids[idx]][2] < lmlist[tipids[idx]-2][2]:
                fingerlist.append(1)
            else:
                fingerlist.append(0)
        
        
        if len(fingerlist)!=0:
            fingercount=fingerlist.count(1)
    
        result['fingerCount'] = fingercount
        result['useHelp'] = True
    else:
        result['fingerCount'] = ''
        result['useHelp'] = True

    return result