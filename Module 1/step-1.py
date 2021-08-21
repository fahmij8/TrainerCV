# =========== Module 1, Step 1.1 : Dataset Taking (Your Face Sample) =========== #
import cv2, sys
import utilities_modul as util

if __name__ == '__main__':
    # Initialize Directory
    util.init_directory(1)

    # Load HAAR face classifier
    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Initialize Webcam
    cap = util.init_camera(util.init_data("urlCamera"))
    count = 0

    # Collect 20 samples of your face from webcam input
    print("[!] Taking samples") 
    while True:
        try:
            ret, frame = cap.read()
            if util.face_extractor(frame, face_classifier) is not None:
                count += 1
                face = cv2.resize(util.face_extractor(frame, face_classifier), (400, 400))

                # Save file in specified directory with unique name
                file_name_path = './dataset/myface/' + str(count) + '.jpg'
                cv2.imwrite(file_name_path, face)

                # Put count on images and display live count
                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                cv2.imshow('Dataset Taker', face)
                
            else:
                print("Face not found")
                pass
            
            if count == 20:
                break
            
            # To quit press q in OpenCV window
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
            
        except:
            print("Unexpected error:", sys.exc_info())
            break   

    cv2.destroyAllWindows()      
    print("[!] Collecting Samples Complete")