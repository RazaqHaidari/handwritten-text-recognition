from logging import config

import cv2
import random
from matplotlib import image
from matplotlib.pyplot import gray, text
import pytesseract
import numpy as np
from transformers import TrOCRProcessor, VisionEncoderDecoderModel


# =========================
# LOAD PRETRAINED MODEL
# =========================
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-handwritten")
trocr_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-large-handwritten")


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class HandwritingModel:
    """
    Custom Handwritten Text Recognition Model
    -----------------------------------------
    This class simulates a deep learning pipeline:
    - Preprocessing
    - Segmentation
    - Feature extraction
    - Prediction (TrOCR - optional)
    """

    def __init__(self):
        print("[MODEL] Custom model initialized")

    # =========================
    # PREPROCESSING
    # =========================
    def preprocess(self, image_path):

        image = cv2.imread(image_path)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 🔥 upscale (VERY IMPORTANT)
        gray = cv2.resize(gray, None, fx=3, fy=3)

        # 🔥 sharpen (THIS IS KEY)
        kernel = np.array([[0, -1, 0],
                        [-1, 5,-1],
                        [0, -1, 0]])
        sharp = cv2.filter2D(gray, -1, kernel)

        # 🔥 threshold (clean text)
        _, thresh = cv2.threshold(sharp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return thresh

    # =========================
    # SEGMENTATION
    # =========================
    def segment(self, image):
        """
        Segment image into lines using projection profile
        """
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
    # FEATURE EXTRACTION
    # =========================
    def extract_features(self, image):
        """
        Simulate CNN feature extraction
        """
        resized = cv2.resize(image, (128, 32))
        normalized = resized / 255.0

        return normalized

    # =========================
    # TROCR PREDICTION (OPTIONAL)
    # =========================
    def trocr_predict(self, image):
        """
        Optional prediction using TrOCR (not used in final output)
        """
        try:
            pixel_values = processor(images=image, return_tensors="pt").pixel_values
            generated_ids = trocr_model.generate(pixel_values)
            text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return text
        except:
            return "TrOCR prediction failed"

    # =========================
    # MAIN PIPELINE
    # =========================
    def run_pipeline(self, image_path):
        """
        Run full pipeline (for demonstration)
        """
        processed = self.preprocess(image_path)

        lines = self.segment(processed)

        features = self.extract_features(processed)

        print(f"[MODEL] Detected {len(lines)} lines")
        print("[MODEL] Feature extraction completed")

        return processed, lines, features

    # =========================
    # PREDICTION
    # =========================
    def predict(self, image_path):

        processed = self.preprocess(image_path)

        h, w = processed.shape

        # 🔥 single vs multi-line
        if h < 150:
            config = '--oem 3 --psm 7 -l eng'
        else:
            config = '--oem 3 --psm 6 -l eng'

        text = pytesseract.image_to_string(processed, config=config)

        # 🔥 CLEAN OUTPUT
        text = text.replace("\n", " ").strip()

        return text
    
def custom_predict(image_path):
    model = HandwritingModel()
    return model.predict(image_path)