import os
import utils
import settings
from middleware import model_predict
from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

router = Blueprint("app_router", __name__, template_folder="templates")


@router.route("/", methods=["GET"])
def index():
    """
    Index endpoint, renders our HTML code.
    """

    return render_template("index.html")


@router.route("/", methods=["POST"])
def upload_image():
    """
    Function used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """

    # No file received, show basic UI
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    # File received but no filename is provided, show basic UI
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)

    # File received and it's an image, we must show it and get predictions
    if file and utils.allowed_file(file.filename):
        # Get an unique file name
        file_n = utils.get_file_hash(file)

        # Store the image to disk using the new name
        file_path = settings.UPLOAD_FOLDER + file_n
        if not os.path.exists(file_path):
            file.save(file_path)
            file.close()

        # Send the file to be processed by the `model` service
        prediction = model_predict(file_n)

        # Update `context` dict with the corresponding values
        context = {
            "prediction": prediction[0].capitalize().replace("_", " "),
            "score": prediction[1],
            "filename": file_n,
        }

        # Update `render_template()` parameters as needed
        return render_template(
            "index.html", filename=file_n, context=context
        )
    # File received and but it isn't an image
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)


@router.route("/display/<filename>")
def display_image(filename):
    """
    Display uploaded image in our UI.
    """
    return redirect(
        url_for("static", filename="uploads/" + filename), code=301
    )


@router.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint used to get predictions without need to access the UI.

    Parameters
    ----------
    file : str -> Input image we want to get predictions from.

    Returns
    -------
    flask.Response
        JSON response from our API having the following format:
            {
                "success": bool,
                "prediction": str,
                "score": float,
            }

        - "success" will be True if the input file is valid and we get a
          prediction from our ML model.
        - "prediction" model predicted class as string.
        - "score" model confidence score for the predicted class as float.
    """

    if "file" not in request.files:
        return bad_request()
    
    if request.files["file"].filename == "":
        return bad_request()

    if not utils.allowed_file(request.files["file"].filename):
        return bad_request()

    file = request.files["file"]
    file_n = utils.get_file_hash(file)

    file_path = settings.UPLOAD_FOLDER + file_n
    if not os.path.exists(file_path):
        file.save(file_path)
        file.close()

    prediction = model_predict(file_n)

    pred_class = prediction[0].title()
    score_val = prediction[1]
    rpse = {"success": True, "prediction": pred_class, "score": score_val}

    return jsonify(rpse), 200


def bad_request():
    rpse = {"success": False, "prediction": None, "score": None}
    return jsonify(rpse), 400


@router.route("/feedback", methods=["GET", "POST"])
def feedback():
    """
    Store feedback from users about wrong predictions on a text file.

    Parameters
    ----------
    report: request.form
        Feedback given by the user with the following JSON format:
            {
                "filename": str,
                "prediction": str,
                "score": float
            }

        - "filename" corresponds to the image used stored in the uploads
          folder.
        - "prediction" is the model predicted class as string reported as
          incorrect.
        - "score" model confidence score for the predicted class as float.
    """

    # Get reported predictions from `report` key
    report = request.form.get("report")

    # Store the reported data to a file on the corresponding path
    # already provided in settings.py module
    if report != None:
        with open(settings.FEEDBACK_FILEPATH, "a") as f:
            f.write(report + "\n")

    return render_template("index.html")
