# =========== Module 3, Step 1 : Preparing color dataset =========== #
import utilities_modul as util
import sys
sys.path.append("/usr/grading")
import grad

if __name__ == '__main__':
    # Read Credential
    usermail = util.init_data("email")

    # Initialize Directory
    util.init_directory(1)
    status = util.prepDataset()
    if(status == True):
        grad.doGrade(usermail, 3, 1)
        print("[!] Dataset preparation success")
    else :
        print(status)