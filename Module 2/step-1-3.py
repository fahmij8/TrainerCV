# =========== Module 1, Step 1.3 : Dataset Taking =========== #
import cv2
import sys, time
import utilities_modul as util

if __name__ == '__main__':
    # Read Credential
    usermail = util.init_data("email")

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

                if count == 20:
                    util.give_grading(usermail=usermail, steps=1)
                    break
                
                # To quit press q in OpenCV window
                if cv2.waitKey(1) & 0xFF == ord('q'): 
                    break
                
            else:
                print("[!] Change your webcam URL if you see this many times.")
        except:
            print("Unexpected error:", sys.exc_info())
            break

    cv2.destroyAllWindows()      
    print("[!] Collecting Samples Complete")
