import pickle
import json
from flask import Flask, request
import numpy as np
import pandas as pd
from database import Database
from utils import Encoder

SAVED_MODEL_PATH = "model_files/house_price_predictor.pkl"
SAVED_LABEL_ENCODER_PATH = "model_files/label_encoder.pkl"

# Loading the classifier and label encoder from file
with open(SAVED_MODEL_PATH, "rb") as f:
    classifier = pickle.load(f)
with open(SAVED_LABEL_ENCODER_PATH, "rb") as f:
    le = pickle.load(f)

app = Flask(__name__)
db = Database()


def __process_input(request_data: json) -> pd.DataFrame:
    """Transforms the provided JSON to a Pandas DataFrame

    Args:
        request_data (json): Input JSON to be transformed

    Returns:
        pd.DataFrame: Input DataFrame
    """

    return pd.DataFrame.from_dict(json.loads(request.data)["inputs"])


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

    # Changing data type of numerical data
    encoder.change_numeric_type()

    # Encoding with an existing LabelEncoder dictionary
    encoder.encode(le)

    # Joining encoded numerical and categorical data
    encoder.join_encoded()

    return encoder.encoded_df


@app.route("/predict", methods=["POST"])
def predict() -> json:
    """
    Takes encoded data about a house and makes a price prediction with a pretrained model.
    Can accept as many house inputs as provided
    """
    input_params = __encode_input(__process_input(request.data))
    try:
        predictions = classifier.predict(input_params)
    except Exception:
        return json.dumps({"error": 'Prediction error'}), 500

    # If prediction is successful, add prediction to database
    try:
        prediction_data = __process_input(request.data)
        prediction_data["predicted price"] = predictions
        db.push_dataframe_to_db("predictions", prediction_data)
    except:
        pass

    return json.dumps({"predicted_prices": predictions.tolist()})


@app.route("/recent_predictions", methods=["GET"])
def recent_predictions() -> json:
    """
    Returns last 10 predictions from the database

    Returns:
        json: last 10 predictions
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

        # Iterate through predictions and form dictionaries, which are later combined to a JSON
        for prediction in db.get_requests_and_responses(10):
            recent_predictions.append(dict(zip(cols, prediction)))
        return json.dumps(recent_predictions, indent=4, ensure_ascii=False)

    except Exception:
        return json.dumps({"error": 'Error loading recent predictions from database'}), 500


if __name__ == "__main__":
    app.run()
