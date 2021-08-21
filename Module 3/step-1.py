# =========== Module 3, Step 1 : Preparing color dataset =========== #
import utilities_modul as util

if __name__ == '__main__':
    # Read Credential
    usermail = util.init_data("email")
    flagGrading = False
    # Initialize Directory
    util.init_directory(1)
    status = util.prepDataset()
    if(status == True and flagGrading == False):
        tryGrad = util.give_grading(usermail=usermail, steps=1)
        if(tryGrad == True):
            flagGrading = True
            print("[!] Dataset preparation success")
    else :
        print(status)
    util.checkGrading(flagGrading)