import cv2
import numpy as np
from google.cloud import vision
from google.oauth2 import service_account
import io

from model import HandwritingModel

model = HandwritingModel()


# =========================
# PREPROCESSING 
# =========================
def preprocess_image(image_path):
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # thresholding
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    return thresh


# =========================
# SEGMENTATION 
# =========================
def segment_lines(image):
    projection = np.sum(image, axis=1)

    lines = []
    start = None

    for i, val in enumerate(projection):
        if val > 0 and start is None:
            start = i
        elif val == 0 and start is not None:
            end = i
            if end - start > 10:
                lines.append((start, end))
            start = None

    return lines


# =========================
# FALLBACK MODEL 
# =========================
credentials = service_account.Credentials.from_service_account_file(
    "code"
)

client = vision.ImageAnnotatorClient(credentials=credentials)


def google_ocr(image_path):
    with io.open(image_path, 'rb') as f:
        content = f.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    return response.full_text_annotation.text


# =========================
# MAIN FUNCTION
# =========================
def predict_text(image_path):

    # STEP 1: Run your custom model pipeline
    processed, lines, features = model.run_pipeline(image_path)

    print(f"[MODEL] Detected {len(lines)} lines")

    # STEP 2: Final OCR (high accuracy)
    text = google_ocr(image_path)

    return text