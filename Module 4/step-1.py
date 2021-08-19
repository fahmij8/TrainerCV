# =========== Module 4, Step 1 : Preparing pre-trained model for object detection =========== #
import utilities_modul as util

if __name__ == '__main__':
    # Prepare pre-trained model
    print("[!] Preparing pre-trained model EfficientDet")
    status = util.downloadData("EfficientDet")
    if (status == True):
        print("[!] Step 1 Completed!")
    else :
        print(f"[!] Step 1 Incompleted, error : {status}")