import pickle
import json
from flask import Flask, request
import numpy as np
import pandas as pd
from database import Database
from utils import Encoder, process_input

SAVED_MODEL_PATH = "model_files/house_price_predictor.pkl"
SAVED_LABEL_ENCODER_PATH = "model_files/label_encoder.pkl"

with open(SAVED_MODEL_PATH, "rb") as f:
    classifier = pickle.load(f)
with open(SAVED_LABEL_ENCODER_PATH, "rb") as f:
    le = pickle.load(f)

app = Flask(__name__)
db = Database()


def __encode_input(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encodes categorical values in input DataFrame to numerical labels

    Args:
        df (pd.DataFrame): Input DataFrame to be encoded

    Returns:
        pd.DataFrame: Encoded DataFrame
    """

    # Create Encoder object with the input DataFrame
    encoder = Encoder(df)

    encoder.change_numeric_type()

    encoder.encode(le)

    encoder.join_encoded()

    return encoder.encoded_df


@app.route("/predict", methods=["POST"])
def predict() -> str:
    """
    Takes encoded data about a house and makes a price prediction with a pretrained model.
    Can accept as many house inputs as provided
    """
    prediction_data = process_input(request.data)
    input_params = __encode_input(prediction_data)
    try:
        predictions = classifier.predict(input_params)
    except Exception as error:
        return json.dumps({"error": "Prediction error"}), 500
    else:
        # If prediction is successful, add prediction to database
        try:
            prediction_data["predicted price"] = predictions
            db.push_dataframe_to_db("predictions", prediction_data)
        except:
            pass

    return json.dumps({"predicted_prices": predictions.tolist()})


@app.route("/recent_predictions", methods=["GET"])
def recent_predictions() -> str:
    """
    Returns last 10 predictions from the database

    Returns:
        str: last 10 predictions
    """
    try:
        cols = [
            "Area",
            "Build year",
            "Building type",
            "Equipment",
            "Floor",
            "Heating system",
            "No. of floors",
            "Number of rooms",
            "Renovation year",
            "city",
            "region",
            "street",
            "price",
        ]
        recent_predictions = []

        # Iterate through predictions and form dictionaries
        for prediction in db.get_requests_and_responses(10):
            recent_predictions.append(dict(zip(cols, prediction)))
        return json.dumps(recent_predictions, indent=4, ensure_ascii=False)

    except Exception as error:
        return (
            json.dumps({"error": "Error loading recent predictions from database"}),
            500,
        )


if __name__ == "__main__":
    app.run()
