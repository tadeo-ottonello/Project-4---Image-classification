import os
import time
import json
import redis
import settings
import numpy as np
from tensorflow.keras.applications import resnet50
from tensorflow.keras.preprocessing import image


db = redis.Redis(
    host = settings.REDIS_IP,
    port = settings.REDIS_PORT,
    db   = settings.REDIS_DB_ID
)

model = resnet50.ResNet50(include_top=True, weights="imagenet")


def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str -> Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """

    path = os.path.join(settings.UPLOAD_FOLDER, image_name)
    img = image.load_img(path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = resnet50.preprocess_input(x)

    preds = model.predict(x)
    preds = resnet50.decode_predictions(preds, top=1)

    prediction = preds[0][0][1]
    score = round(float(preds[0][0][2]), 4)

    return prediction, score


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        _, msg = db.brpop(settings.REDIS_QUEUE)
        msg = json.loads(msg)

        id = msg["id"]
        image_name = msg["image_name"]

        prediction, score = predict(image_name)

        pred_dict = {"prediction":prediction, "score":score}

        db.set(id, json.dumps(pred_dict))

        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    print("Launching ML service...")
    classify_process()
