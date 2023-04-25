
import tempfile
import shutil

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

FILE_UPLOAD_DIR = BASE_DIR

def handle_uploaded_file(source):
    fd, filepath = tempfile.mkstemp(prefix=source.name, dir=FILE_UPLOAD_DIR)
    with open(filepath, 'wb') as dest:
        shutil.copyfileobj(source, dest)
    return filepath