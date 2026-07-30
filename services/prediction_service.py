import numpy as np
import tensorflow as tf
from PIL import Image
from pathlib import Path


# =========================================================
# MODEL
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "assets"
    / "models"
    / "skin_cancer_model.h5"
)


# =========================================================
# CLASS NAMES
# =========================================================

CLASS_NAMES = [
    "Actinic Keratoses",
    "Basal Cell Carcinoma",
    "Benign Keratosis",
    "Dermatofibroma",
    "Melanoma",
    "Nevus",
    "Vascular Lesion"
]


# =========================================================
# LOAD MODEL
# =========================================================

_model = None


def load_skin_model():

    global _model

    if _model is None:

        if not MODEL_PATH.exists():

            raise FileNotFoundError(
                f"Model file not found: {MODEL_PATH}"
            )

        _model = tf.keras.models.load_model(
            MODEL_PATH,
            compile=False
        )

    return _model


# =========================================================
# PREDICT SKIN
# =========================================================

def predict_skin(image):

    model = load_skin_model()

    # Make sure image is RGB
    image = image.convert("RGB")

    # Model input: (75, 100, 3)
    image = image.resize((100, 75))

    # Convert image to numpy
    image_array = np.array(image, dtype=np.float32)

    # Normalize pixel values
    image_array = image_array / 255.0

    # Add batch dimension
    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # Prediction
    predictions = model.predict(
        image_array,
        verbose=0
    )

    # Get highest probability
    predicted_index = int(
        np.argmax(predictions[0])
    )

    confidence = float(
        predictions[0][predicted_index] * 100
    )

    disease = CLASS_NAMES[predicted_index]

    return {
        "disease": disease,
        "confidence": round(confidence, 2)
    }