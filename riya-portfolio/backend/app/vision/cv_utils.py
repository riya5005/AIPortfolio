import cv2
import numpy as np
import base64
from app.vision.dl_classifier import classify_image

# OpenCV ships this classifier file built-in — no download required.
_face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def _decode_image(image_bytes: bytes) -> np.ndarray:
    np_arr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


def _encode_image(img: np.ndarray) -> str:
    """Encode an OpenCV image back to a base64 string for sending to the frontend."""
    _, buffer = cv2.imencode(".jpg", img)
    return base64.b64encode(buffer).decode("utf-8")


def analyze_image(image_bytes: bytes) -> dict:
    """
    Runs basic computer vision analysis on an uploaded image:
      - grayscale conversion
      - Canny edge detection
      - Haar cascade face detection

    Returns stats plus base64-encoded processed images for display.
    """
    img = _decode_image(image_bytes)
    if img is None:
        raise ValueError("Could not decode image — unsupported format or corrupted file.")

    height, width = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, 100, 200)
    edge_pixel_ratio = round(float(np.count_nonzero(edges)) / edges.size, 4)

    # Face detection
    faces = _face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw boxes around detected faces on a copy of the original image
    annotated = img.copy()
    for (x, y, w, h) in faces:
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 3)

    return {
        "width": int(width),
        "height": int(height),
        "faces_detected": int(len(faces)),
        "edge_pixel_ratio": edge_pixel_ratio,
        "annotated_image_base64": _encode_image(annotated),
        "edges_image_base64": _encode_image(edges),
    }
