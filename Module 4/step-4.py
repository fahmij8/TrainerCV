# =========== Module 4, Step 4 : Testing Model =========== #
import tensorflow_hub as hub
import tensorflow as tf
import cv2
import sys
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
    model = tf.keras.models.load_model('model_module-4.h5')

    # Prepare label
    label_path = "./efficientdet_labels.csv"
    label = pd.read_csv(label_path, sep=';', index_col='ID')
    labels = label['OBJECT (2017 REL.)']

    # Initialize camera
    cap = util.init_camera(util.init_data("urlCamera"))
    img_boxes = None

    while True:
        try:
            ret, frame = cap.read()
            img = cv2.resize(frame, (800, 600))
            rgb_tensor = tf.convert_to_tensor(img, dtype=tf.uint8)
            rgb_tensor = tf.expand_dims(rgb_tensor, 0)
            boxes, scores, classes, num_detection = detector(rgb_tensor)
            pred_labels = classes.numpy().astype('int')[0]
            pred_labels = [labels[i] for i in pred_labels]
            pred_boxes = boxes.numpy()[0].astype('int')
            pred_scores = scores.numpy()[0]
            detectAny = False
            for score, (ymin, xmin, ymax, xmax), label in zip(pred_scores, pred_boxes, pred_labels):
                if score < 0.5:
                    continue
                if (label == 'apple' or label == 'orange' or label == 'banana'):
                    detectAny = True
                    obj = cv2.resize(img[ymin:ymax, xmin:xmax], (224, 224))
                    im = Image.fromarray(obj, 'RGB')
                    img_array = np.array(im)
                    img_array = np.expand_dims(img_array, axis=0)
                    pred = model.predict(img_array)
                    result = np.argmax(pred)
                    confidence = int(pred[0][result] * 100)
                    tags = ['Fresh Apples','Fresh Banana', 'Fresh Orange', 'Rotten Apples', 'Rotten Banana', 'Rotten Orange']
                    img_boxes = cv2.rectangle(img, (xmin, ymin), (xmax,ymax), (0,255,0), 2)
                    labelToShow = f"{tags[result]} : {confidence}%"
                    (text_width, text_height) = cv2.getTextSize(labelToShow, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, thickness=2)[0]
                    cv2.rectangle(img_boxes, (xmin, ymin-20), (xmin+text_width, ymin+text_height-15), (0, 255, 0), -1)
                    cv2.putText(img_boxes, labelToShow, (xmin, ymin-6), cv2.FONT_HERSHEY_SIMPLEX,  0.6, (255, 255, 255), 2 )
                    util.postRequest(confidence, appName, deviceName, key)
                    # cv2.putText(img_boxes, f"EfficientDet => {label} : {100 * round(score)}%", (xmin+10, ymax-20), cv2.FONT_HERSHEY_SIMPLEX,  0.4, (255, 255, 255), 2 )
            if(detectAny):
                cv2.imshow("Object Detection",	img_boxes)
            else:
                cv2.imshow("Object Detection",	img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    cv2.destroyAllWindows()
    print("[!] Testing Model Complete")