import cv2
import os, shutil, json, requests, zipfile, io

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
    payload = "{\r\n    \"m2m:cin\": {\r\n    \"con\": \"{\\\"color\\\":" + str(predict) + "}\"\r\n    }\r\n}"
    headers = {
        'x-m2m-origin': key,
        'content-type': "application/json;ty=4",
        'accept': "application/json",
        'cache-control': "no-cache",
        'postman-token': "e10b0cdc-98bc-4459-be34-25417d5f57bd"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response

def prepDataset():
        r = requests.get("https://firebasestorage.googleapis.com/v0/b/trainercv-dpte.appspot.com/o/datasets%2Fmodule-3.zip?alt=media&token=d7c2549d-1a30-41dd-89aa-d3de034dd09f")
        if(r.status_code == 200):
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall()
            return True
        else :
            return "[!] Dataset preparation failed, please re-run the code or contact admin for further information"