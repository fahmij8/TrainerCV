# =========== Module 4, Step 1 : Preparing pre-trained model for object detection =========== #
import utilities_modul as util

if __name__ == '__main__':
    # Read Credential
    usermail = util.init_data("email")

    # Prepare pre-trained model
    print("[!] Preparing pre-trained model EfficientDet")
    status = util.downloadData("EfficientDet")
    if (status == True):
        util.give_grading(usermail=usermail, steps=1, optionalParam=status)
    else :
        print(f"[!] Step 1 Incompleted, error : {status}")