# =========== Module 4, Step 4 : Testing Model with IoT impelementation =========== #
import tensorflow_hub as hub
import tensorflow as tf
import cv2
import sys, os
import pandas as pd
import numpy as np
import utilities_modul as util
from PIL import Image

if __name__ == '__main__':
    # Read Credential
    usermail = util.init_data("email")
    appName = util.init_data("appName")
    deviceName = util.init_data("deviceName")
    key = util.init_data("xm2morigin")

    # Prepare pre-trained model
    print("[!] Load EfficientDet")
    detector = hub.KerasLayer("./efficientdet/")

    # Prepare fruit freshness model
    print("[!] Load Fruit Freshness Model")
    if(os.path.isfile('model_module-4.h5')):
        util.give_grading(usermail=usermail, steps=2, optionalParam=True)
        model = tf.keras.models.load_model('model_module-4.h5')
    else:
        sys.exit('[!] Model is not available!')

    # Prepare label
    label_path = "./efficientdet_labels.csv"
    label = pd.read_csv(label_path, sep=';', index_col='ID')
    labels = label['OBJECT (2017 REL.)']

    # Initialize camera
    cap = util.init_camera(util.init_data("urlCamera"))
    img_boxes = None
    detectedTimes = 0

    while True:
        try:
            ret, frame = cap.read()

            # Image pre-processing
            # Resize frame to desired object detection image size
            img = cv2.resize(frame, (800, 600))
            # Convert image to tensor and expand its dimension
            rgb_tensor = tf.convert_to_tensor(img, dtype=tf.uint8)
            rgb_tensor = tf.expand_dims(rgb_tensor, 0)

            # Detect object using EfficientDef
            boxes, scores, classes, num_detection = detector(rgb_tensor)
            
            # Store boxes coordinates, object scores/confidence, object class, and number detection
            pred_labels = classes.numpy().astype('int')[0]
            pred_labels = [labels[i] for i in pred_labels]
            pred_boxes = boxes.numpy()[0].astype('int')
            pred_scores = scores.numpy()[0]
            detectAny = False

            # Iterate through result
            for score, (ymin, xmin, ymax, xmax), label in zip(pred_scores, pred_boxes, pred_labels):
                # If confidence less than 0.5, nothing get's executed
                if score < 0.5:
                    continue

                # If confidence more than 0.5 and the label is listed below
                if (label == 'apple' or label == 'orange' or label == 'banana'):
                    detectAny = True
                    detectedTimes += 1

                    # Preprocess image (again) for fruit model
                    # Resize image
                    obj = cv2.resize(img[ymin:ymax, xmin:xmax], (224, 224))
                    # Convert image to array
                    im = Image.fromarray(obj, 'RGB')
                    img_array = np.array(im)
                    img_array = np.expand_dims(img_array, axis=0)
                    # Predict the fruit!
                    pred = model.predict(img_array)
                    print(f'{detectedTimes} => {pred}')
                    # Determine which label is having bigger confidence
                    result = np.argmax(pred)
                    confidence = int(pred[0][result] * 100)
                    # Show result in boxes and labels
                    tags = ['Fresh Apples','Fresh Banana', 'Fresh Orange', 'Rotten Apples', 'Rotten Banana', 'Rotten Orange']
                    img_boxes = cv2.rectangle(img, (xmin, ymin), (xmax,ymax), (0,255,0), 2)
                    labelToShow = f"{tags[result]} : {confidence}%"
                    (text_width, text_height) = cv2.getTextSize(labelToShow, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, thickness=2)[0]
                    cv2.rectangle(img_boxes, (xmin, ymin-20), (xmin+text_width, ymin+text_height-15), (0, 255, 0), -1)
                    cv2.putText(img_boxes, labelToShow, (xmin, ymin-6), cv2.FONT_HERSHEY_SIMPLEX,  0.6, (255, 255, 255), 2 )
                    # cv2.putText(img_boxes, f"EfficientDet => {label} : {100 * round(score)}%", (xmin+10, ymax-20), cv2.FONT_HERSHEY_SIMPLEX,  0.4, (255, 255, 255), 2 )
                    # Send the result to Antares
                    util.postRequest(confidence, appName, deviceName, key)

            # If listed object were detected, show it's result
            if(detectAny):
                cv2.imshow("Object Detection",	img_boxes)
            # Otherwise, show the original image
            else:
                cv2.imshow("Object Detection",	img)
            
            # To quit press q in OpenCV window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                util.give_grading(usermail=usermail, steps=4, optionalParam=detectedTimes)
                break
        
        # Error handling
        except:
            print("Unexpected error:", sys.exc_info()[0])
            break

    cv2.destroyAllWindows()
    print("[!] Testing Model Complete")