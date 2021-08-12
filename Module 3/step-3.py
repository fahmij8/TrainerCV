# =========== Module 1, Step 3 : Model Testing =========== #
import cv2, sys
import tensorflow as tf
import numpy as np
import utilities_modul as util
# sys.path.append("/usr/grading")
# import grad
from PIL import Image

if __name__ == '__main__':
    # Read Credential
    usermail = util.init_data("email")

    # Load Models
    model = tf.keras.models.load_model('model_module-3.h5')

    # Initialize Webcam
    cap = util.init_camera(util.init_data("urlCamera"))

    # Testing Model
    while True:
        try:
            ret, frame = cap.read()
            # frame [y:y+h, w:w+h]
            cv2.rectangle(frame, (100, 300), (300, 100), (255, 0, 0), 2)
            roi = frame[100:300, 100:300]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            i = 0
            # list for storing names of shapes
            for contour in contours:
                # here we are ignoring first counter because 
                # findcontour function detects whole image as shape
                if i == 0:
                    i = 1
                    continue
            
                # cv2.approxPloyDP() function to approximate the shape
                approx = cv2.approxPolyDP(
                    contour, 0.01 * cv2.arcLength(contour, True), True)
                    
                if len(approx) == 3 :
                    obj = cv2.resize(roi, (150, 150))
                    im = Image.fromarray(obj, 'RGB')
                    img_array = np.array(im)
                    img_array = np.expand_dims(img_array, axis=0)
                    pred = model.predict(img_array)
                    result = np.argmax(pred)
                    confidence = int(pred[0][result] * 100)
                    print(f"Triangle with color of {result} = {confidence}")    

                # using drawContours() function
                cv2.drawContours(roi, [approx], 0, (0, 0, 255), 5)
                
                            
                
            frame[100:300, 100:300] = roi
            cv2.imshow("contours",	frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    cv2.destroyAllWindows()
    print("[!] Testing Model Complete")