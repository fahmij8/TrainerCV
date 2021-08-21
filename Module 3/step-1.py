# =========== Module 3, Step 1 : Preparing color dataset =========== #
import utilities_modul as util

if __name__ == '__main__':
    # Read Credential
    usermail = util.init_data("email")
    
    # Initialize Directory
    util.init_directory(1)
    status = util.prepDataset()
    if(status == True):
        util.give_grading(usermail=usermail, steps=1, optionalParam=status)
    else :
        print(status)