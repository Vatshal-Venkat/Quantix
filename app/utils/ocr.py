from PIL import Image
import pytesseract
import cv2
import numpy as np
import io
import os

# Windows-only: set tesseract path if needed
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )


def extract_text_from_image(image_bytes: bytes) -> dict:
    """
    Performs OCR using Tesseract.
    Returns extracted text + confidence score.
    """

    # Load image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Convert to OpenCV format
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Preprocessing (IMPORTANT for math text)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    # OCR with confidence data
    data = pytesseract.image_to_data(
        gray,
        output_type=pytesseract.Output.DICT,
        config="--psm 6"
    )

    words = []
    confidences = []

    for i, text in enumerate(data["text"]):
        if text.strip():
            words.append(text)
            conf = int(data["conf"][i])
            if conf > 0:
                confidences.append(conf)

    extracted_text = " ".join(words)
    avg_confidence = (
        sum(confidences) / len(confidences)
        if confidences else 0
    )

    return {
        "text": extracted_text,
        "confidence": avg_confidence
    }
