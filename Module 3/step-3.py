# =========== Module 3, Step 3 : Model Testing =========== #
import cv2, sys
import tensorflow as tf
import numpy as np
import utilities_modul as util
from PIL import Image

if __name__ == '__main__':
    # Read Credential
    usermail = util.init_data("email")

    # Load Models
    model = tf.keras.models.load_model('model_module-3.h5')

    # Initialize Webcam
    cap = util.init_camera(util.init_data("urlCamera"))
    detectedTimes = 60

    # Testing Model
    while True:
        try:
            flagGrading = False
            ret, frame = cap.read()
            # Create region of interest
            cv2.rectangle(frame, (100, 300), (300, 100), (255, 0, 0), 2)
            # Take images inside the ROI [y:y+h, w:w+h]
            roi = frame[100:300, 100:300]
            # Filter image to gray
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            # Find image contour
            _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            maskTriangle = roi.copy()
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
                if len(approx) == 3 :
                    detectedTimes -= 1
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

                    # Image pre-processing, sharpen image
                    first_array = np.array([[0, 0, 0],
                                            [0, 2, 0],
                                            [0, 0, 0]])
                    second_array = np.ones((3, 3), np.float32) / 9
                    kernel = first_array - second_array
                    filtered = cv2.filter2D(obj,-1,kernel)

                    # Image pre-processing, turn images to numpy array
                    im = Image.fromarray(filtered, 'RGB')
                    img_array = np.array(im)
                    img_array = np.expand_dims(img_array, axis=0)

                    # Predict the images
                    pred = model.predict(img_array)

                    # Determine which label the images fall for
                    result = np.argmax(pred)
                    confidence = int(pred[0][result] * 100)
                    colors = ['black','blue','brown','green','grey','orange','red','violet','white','yellow']

                    # Showing image and text
                    cv2.imshow("Cropped", obj)
                    cv2.putText(roi, f'{colors[result]} Triangle ({confidence}%)', (xtags, ytags), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
                # Showing image contour
                cv2.drawContours(roi, [approx], -1, (0, 0, 255), 2)

            # Re-apply contour to ROI area    
            frame[100:300, 100:300] = roi

            # Show frame
            cv2.imshow("contours",	frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            flagGrading = None
            print("Unexpected error:", sys.exc_info()[0])
            raise

    cv2.destroyAllWindows()
    print("[!] Testing Model Complete")