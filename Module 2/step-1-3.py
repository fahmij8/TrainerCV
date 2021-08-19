# =========== Module 1, Step 1.3 : Dataset Taking =========== #
import cv2
import sys, time
import utilities_modul as util
sys.path.append("/usr/grading")
import grad

if __name__ == '__main__':
    # Read Credential
    usermail = util.init_data("email")
    flagGraded = None

    # Directory Initialization
    util.init_directory(3)

    # Initialize Webcam
    cap = util.init_camera(util.init_data("urlCamera"))
    count = 0

    # Collect 20 samples of your face from webcam input
    print("[!] Taking samples") 
    while True:
        try:
            ret, frame = cap.read()
            if frame is not None:
                empty = cv2.resize(frame, (400, 400))

                # Save file in specified directory with unique name
                file_name_path = './dataset/empty/' + str(count) + '.jpg'
                cv2.imwrite(file_name_path, empty)
                count += 1
                
                # Put count on images and display live count
                cv2.putText(empty, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                cv2.imshow('Dataset Taker', empty)
                time.sleep(1)

                if cv2.waitKey(1) == 13: #Break with CTRL + C or Finish take dataset with 20 sample
                    flagGraded = False
                    break
                elif count == 20:
                    flagGraded = True
                    grad.doGrade(usermail, 2, 1)
                    break
            else:
                print("[!] Change your webcam URL if you see this many times.")
        except:
            print("[!] Change your webcam URL if you see this many times.")
            pass

    cv2.destroyAllWindows()      
    print("[!] Collecting Samples Complete")
    if(flagGraded == False):
        print("[!] You're not graded due to an error. Finish your dataset taking.")