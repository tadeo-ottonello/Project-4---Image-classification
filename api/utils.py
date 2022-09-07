import os
import hashlib


def allowed_file(filename):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files.

    Parameters
    ----------
    filename : str -> Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool -> True if the file is an image, False otherwise.
    """

    ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif"}
    ext = os.path.splitext(filename)[1].lower()

    valid_file = ext in ALLOWED_EXTENSIONS
    return valid_file


def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage -> File sent by user.

    Returns
    -------
    str -> New filename based in md5 file hash.
    """

    hash_data = hashlib.md5(file.read()).hexdigest()
    file.seek(0)

    ext = os.path.splitext(file.filename)[1].lower()

    hash_name = hash_data + ext

    return hash_name