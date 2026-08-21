import numpy as np
import cv2

_model = None


def _get_model():
    global _model
    if _model is None:
        # into memory the first time someone actually uses this feature.
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.applications.mobilenet_v2 import decode_predictions
        global _decode_predictions
        _decode_predictions = decode_predictions
        _model = MobileNetV2(weights="imagenet")
    return _model


def classify_image(img: np.ndarray) -> list[dict]:
    """
    Takes an OpenCV-loaded image (BGR, as from cv2.imdecode) and returns
    the top-3 predicted labels with confidence scores.
    """
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

    model = _get_model()

    resized = cv2.resize(img, (224, 224))
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    batch = np.expand_dims(rgb, axis=0).astype("float32")
    batch = preprocess_input(batch)

    predictions = model.predict(batch, verbose=0)
    decoded = _decode_predictions(predictions, top=3)[0]

    return [
        {"label": label.replace("_", " "), "confidence": round(float(score), 4)}
        for (_, label, score) in decoded
    ]
