import cv2
import os, shutil, json, requests, zipfile, tarfile, sys
from tqdm import tqdm
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
    payload = "{\r\n    \"m2m:cin\": {\r\n    \"con\": \"{\\\"confidence\\\":" + str(predict) + "}\"\r\n    }\r\n}"
    headers = {
        'x-m2m-origin': key,
        'content-type': "application/json;ty=4",
        'accept': "application/json",
        'cache-control': "no-cache",
        'postman-token': "e10b0cdc-98bc-4459-be34-25417d5f57bd"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response

def downloadData(mode):
        if(mode == "EfficientDet"):
            url = "https://firebasestorage.googleapis.com/v0/b/trainercv-dpte.appspot.com/o/EfficientDet.zip?alt=media&token=ab072dab-e9ba-4ef8-9bb4-a165ab68d48e"
            filename = 'EfficientDet.zip'
        elif(mode == "FruitModel"):
            url = "https://firebasestorage.googleapis.com/v0/b/trainercv-dpte.appspot.com/o/model_module-4.zip?alt=media&token=5d053d40-a254-4959-8511-c23ab8fb9472"
            filename = 'model_module-4.zip'
        
        response = requests.get(url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        block_size = 1024 #1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(filename, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")
        if(os.path.exists(filename)) :
            z = zipfile.ZipFile(filename)
            z.extractall()
            if(mode == "EfficientDet"):
                tar = tarfile.open("efficientdet_lite2_detection_1.tar.gz", "r:gz")
                tar.extractall(path="./efficientdet")
                tar.close()
            return True
        return "[!] Pre-trained model preparation failed, please re-run the code or contact admin for further information"

def give_grading(usermail, steps, optionalParam):
    steps = int(steps)
    if(isinstance(optionalParam, list)):
        status = grad.doGrade(usermail, 4, steps, optionalParam)
    else:
        status = grad.doGrade(usermail, 4, steps)
    return status

def checkGrading(flagGrading):
    if(flagGrading == False):
        print("[!] You're not graded due to an error. Repeat this step with the fixing note above, if error still occur please contact administrator")