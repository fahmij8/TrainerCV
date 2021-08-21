import cv2
import os, shutil, json, requests, sys
from mediapipe.python.solutions.hands import HandLandmark
from mediapipe.python.solutions.drawing_utils import DrawingSpec
sys.path.append("/usr/grading")
import grad

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
    return response

def landmark_style_index():
    _PALM_LANMARKS = (HandLandmark.WRIST, HandLandmark.THUMB_CMC,
                    HandLandmark.INDEX_FINGER_MCP, HandLandmark.MIDDLE_FINGER_MCP,
                    HandLandmark.RING_FINGER_MCP, HandLandmark.PINKY_MCP)
    _THUMP_LANDMARKS = (HandLandmark.THUMB_MCP, HandLandmark.THUMB_IP,
                        HandLandmark.THUMB_TIP)
    _INDEX_FINGER_LANDMARKS = (HandLandmark.INDEX_FINGER_PIP,
                            HandLandmark.INDEX_FINGER_DIP)
    _INDEX_FINGER_TIP_LANDMARKS = (HandLandmark.INDEX_FINGER_TIP, HandLandmark.INDEX_FINGER_TIP)
    _MIDDLE_FINGER_LANDMARKS = (HandLandmark.MIDDLE_FINGER_PIP,
                                HandLandmark.MIDDLE_FINGER_DIP,
                                HandLandmark.MIDDLE_FINGER_TIP)
    _RING_FINGER_LANDMARKS = (HandLandmark.RING_FINGER_PIP,
                            HandLandmark.RING_FINGER_DIP,
                            HandLandmark.RING_FINGER_TIP)
    _PINKY_FINGER_LANDMARKS = (HandLandmark.PINKY_PIP, HandLandmark.PINKY_DIP,
                            HandLandmark.PINKY_TIP)
    
    _RADIUS = 5
    _RED = (48, 48, 255)
    _GREEN = (48, 255, 48)
    _BLUE = (192, 101, 21)
    _YELLOW = (0, 204, 255)
    _GRAY = (128, 128, 128)
    _PURPLE = (128, 64, 128)
    _PEACH = (180, 229, 255)
    _WHITE = (224, 224, 224)

    # Hands
    _THICKNESS_WRIST_MCP = 3
    _THICKNESS_FINGER = 2
    _THICKNESS_DOT = -1

    _HAND_LANDMARK_STYLE = {
        _PALM_LANMARKS:
            DrawingSpec(
                color=_RED, thickness=_THICKNESS_DOT, circle_radius=_RADIUS),
        _THUMP_LANDMARKS:
            DrawingSpec(
                color=_RED, thickness=_THICKNESS_DOT, circle_radius=_RADIUS),
        _INDEX_FINGER_LANDMARKS:
            DrawingSpec(
                color=_RED, thickness=_THICKNESS_DOT, circle_radius=_RADIUS),
        _INDEX_FINGER_TIP_LANDMARKS:
            DrawingSpec(
                color=_YELLOW, thickness=_THICKNESS_DOT, circle_radius=_RADIUS+3),
        _MIDDLE_FINGER_LANDMARKS:
            DrawingSpec(
                color=_RED, thickness=_THICKNESS_DOT, circle_radius=_RADIUS),
        _RING_FINGER_LANDMARKS:
            DrawingSpec(
                color=_RED, thickness=_THICKNESS_DOT, circle_radius=_RADIUS),
        _PINKY_FINGER_LANDMARKS:
            DrawingSpec(
                color=_RED, thickness=_THICKNESS_DOT, circle_radius=_RADIUS),
    }

    hand_landmark_style = {}
    for k, v in _HAND_LANDMARK_STYLE.items():
        for landmark in k:
            hand_landmark_style[landmark] = v
    return hand_landmark_style


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

def give_grading(usermail, steps, optionalParam):
    steps = int(steps)
    if(isinstance(optionalParam, list)):
        status = grad.doGrade(usermail, 5, steps, optionalParam)
    else:
        status = grad.doGrade(usermail, 5, steps)
    return status

def checkGrading(flagGrading):
    if(flagGrading == False):
        print("[!] You're not graded due to an error. Repeat this step with the fixing note above, if error still occur please contact administrator")