# =========== Module 3, Step 3 : Model Testing =========== #
import cv2, traceback
import tensorflow as tf
import numpy as np
import utilities_modul as util
from PIL import Image

if __name__ == '__main__':
    # Clear memory
    util.init_clearmemory()

    # Read Credential
    usermail = util.init_data("email")

    # Load Models
    model = tf.keras.models.load_model('model_module-3.h5')

    # Initialize Webcam
    cap = util.init_camera(util.init_data("urlCamera"))
    detectedTimes = 0

    # Testing Model
    while True:
        try:
            flagGrading = False
            ret, frame = cap.read()
            # Filter image to gray
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Find image contour
            _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            maskTriangle = frame.copy()
            i = 0
            
            for index, contour in enumerate(contours):
                # here we are ignoring first counter because 
                # findcontour function detects whole image as shape
                if i == 0:
                    i = 1
                    continue
            
                # cv2.approxPloyDP() function to approximate the shape
                approx = cv2.approxPolyDP(
                    contour, 0.01 * cv2.arcLength(contour, True), True)
                
                # Determine center of the triangle to put text
                M = cv2.moments(contour)
                if M['m00'] != 0.0:
                    xtags = int(M['m10']/M['m00'])
                    ytags = int(M['m01']/M['m00'])
                else:
                    xtags = 0
                    ytags = 0

                # If shape approximation equals to triangle (having 3 corner)
                if len(approx) == 3 and cv2.contourArea(contours[index]) > 350 :
                    detectedTimes += 1
                    # Mask out the triangle
                    mask = np.zeros_like(maskTriangle)
                    cv2.drawContours(mask, contours, index,  (255, 255, 255), -1)
                    out = np.zeros_like(maskTriangle)
                    out[mask == 255] = maskTriangle[mask == 255]

                    # Cut the image of the triangle itself (to predict its color)
                    (y, x, channel) = np.where(mask == 255)
                    (topy, topx) = (np.min(y), np.min(x))
                    (bottomy, bottomx) = (np.max(y), np.max(x))
                    out = out[topy:bottomy+1, topx:bottomx+1]

                    # Image pre-processing, resize image
                    obj = cv2.resize(out, (200, 200))
                    obj = cv2.cvtColor(obj, cv2.COLOR_BGR2RGB)

                    # Image pre-processing, turn images to numpy array
                    x = tf.keras.preprocessing.image.img_to_array(obj)
                    x /= 255
                    x = np.expand_dims(x, axis=0)
                    images = np.vstack([x])

                    # Predict the images
                    pred = model.predict(images)
                    print(f'{detectedTimes} => {pred}')
                    
                    # Determine which label the images fall for
                    result = np.argmax(pred)
                    confidence = int(pred[0][result] * 100)
                    colors = ['black','blue','brown','green','grey','orange','red','violet','white','yellow']

                    # Showing image and text
                    obj = cv2.cvtColor(obj, cv2.COLOR_RGB2BGR)
                    cv2.imshow("Cropped", obj)
                    cv2.putText(frame, f'{colors[result]} Triangle ({confidence}%)', (xtags, ytags), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    
                    # Showing image contour
                    cv2.drawContours(frame, [approx], -1, (0, 0, 255), 2)

            # Show frame
            cv2.imshow("contours",	frame)

            # To quit press q in OpenCV window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                util.give_grading(usermail=usermail, steps=3, optionalParam=detectedTimes)
                break
        except:
            print("Unexpected error:", traceback.format_exc())
            break

    cv2.destroyAllWindows()
    print("[!] Testing Model Complete")