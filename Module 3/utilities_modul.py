import cv2
import os, shutil, json, requests, zipfile, sys
from tqdm import tqdm

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
    url = "https://platform.antares.id:8443/~/antares-cse/antares-id/" + appname + "/" + devicename
    payload = json.dumps({
        "m2m:cin" : {
            "con" : json.dumps({
                "color" : str(predict)
            })
        }
    })
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
        print("Package not sended")
        sys.exit()

def prepDataset():
    url = "https://firebasestorage.googleapis.com/v0/b/trainercv-dpte.appspot.com/o/datasets%2Fmodule-3.zip?alt=media&token=d7c2549d-1a30-41dd-89aa-d3de034dd09f"
    filename = 'module-3.zip'
    if(not os.path.isfile(filename)):
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
            return True
        return "[!] Pre-trained model preparation failed, please re-run the code or contact admin for further information"
    else:
        print(f"[!] File module-3.zip is already available")
        return True


def give_grading(usermail, steps, *args, **kwargs):
    optionalParam = kwargs.get('optionalParam')
    payload = json.dumps({
        "usermail": usermail,
        "steps": steps,
        "optionalParam": optionalParam
    })
    
    url = "https://trainercv-grading.herokuapp.com/grad-module-3"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    if(response.status_code == 200):
        print(json.loads(response.text)['message'])
    else:
        sys.exit()