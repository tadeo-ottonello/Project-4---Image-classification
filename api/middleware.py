import time
import uuid
import redis
import json
import settings

# Redis connection
db = redis.Redis(
    host = settings.REDIS_IP,
    port = settings.REDIS_PORT,
    db = settings.REDIS_DB_ID
)


def model_predict(image_name):
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    image_name : str -> Name for the image uploaded by the user.

    Returns
    -------
    prediction, score : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    # Assign an unique ID for this job to be able to keep track of it across all the services.
    job_id = str(uuid.uuid4())

    # Creation of a dict with the job data we will send through Redis.
    job_data = {
       "id": job_id,
       "image_name": image_name,
    }

    msg_str = json.dumps(job_data)

    # Send the job to the model service using Redis.
    db.rpush(
        settings.REDIS_QUEUE,
        msg_str
    )

    # Loop until we received the response from our ML model
    while True:
        if db.get(job_id):
            output = db.get(job_id)
            output = json.loads(output)
            prediction = output["prediction"]
            score = output["score"]

            db.delete(job_id)
            break

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return prediction, score
