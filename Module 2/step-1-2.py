# =========== Module 2, Step 1.2 : Dataset Taking (Another Face Sample) =========== #
import cv2
import utilities_modul as util

if __name__ == '__main__':
    # Initialize Directory
    util.init_directory(2)

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
                file_name_path = './dataset/secondface/' + str(count) + '.jpg'
                cv2.imwrite(file_name_path, face)

                # Put count on images and display live count
                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                cv2.imshow('Dataset Taker', face)
                
            else:
                print("Face not found")
                pass

            if cv2.waitKey(1) == 13 or count == 20: 
                break
        except:
            print("[!] Change your webcam URL if you see this many times.")
            pass    

    cv2.destroyAllWindows()      
    print("[!] Collecting Samples Complete")