import pickle
import json
from flask import Flask, request
import numpy as np
import pandas as pd
from database import Database
from sklearn import preprocessing

SAVED_MODEL_PATH = "model_files/house_price_predictor.pkl"
SAVED_LABEL_ENCODER_PATH = "model_files/label_encoder.pkl"

# Loading the classifier and label encoder from file
with open(SAVED_MODEL_PATH, "rb") as f:
    classifier = pickle.load(f)
with open(SAVED_LABEL_ENCODER_PATH, "rb") as f:
    le = pickle.load(f)

app = Flask(__name__)
db = Database()


def __process_input(request_data: list) -> pd.DataFrame:
    """
    Transforms the provided JSON to a Pandas DataFrame
    """
    return pd.DataFrame.from_dict(json.loads(request.data)["inputs"])


def __encode_input(data: pd.DataFrame) -> pd.DataFrame:
    """
    Encodes categorical values in input DataFrame to numerical labels

    Args:
        data (pd.DataFrame): Input DataFrame to be encoded

    Returns:
        pd.DataFrame: Encoded DataFrame
    """
    data = data.astype(
        {
            "Area": "float64",
            "Build year": "int64",
            "Floor": "int64",
            "No. of floors": "int64",
            "Renovation year": "int64",
            "Number of rooms": "int64",
        }
    )

    encoded_data = data[
        [
            "Area",
            "Build year",
            "Floor",
            "No. of floors",
            "Number of rooms",
            "Renovation year",
        ]
    ]

    # Categorical data to be encoded
    categorical_data = data[
        [
            "Building type",
            "Equipment",
            "Heating system",
            "city",
            "region",
            "street",
        ]
    ]

    # Encoding categorical data with Scikit-Learn LabelEncoder
    categorical_columns = [
        "Building type",
        "Equipment",
        "Heating system",
        "city",
        "region",
        "street",
    ]

    try:
        for col in categorical_columns:
            categorical_data[col] = le[col].transform(categorical_data[col])
    except Exception as error:
        return json.dumps({"error": str(error)}), 400

    # Joining encoded numerical and categorical data
    return encoded_data.join(categorical_data)


@app.route("/predict", methods=["POST"])
def predict() -> list:
    """
    Takes encoded data about a house and makes a price prediction with a pretrained model.
    Can accept as many house inputs as provided
    """
    input_params = __encode_input(__process_input(request.data))
    try:
        predictions = classifier.predict(input_params)
    except Exception as error:
        return json.dumps({"error": str(error)}), 400

    # If prediction is successful, add prediction to database
    prediction_data = __process_input(request.data)
    prediction_data["predicted price"] = predictions
    db.push_dataframe_to_db("predictions", prediction_data)

    return json.dumps({"predicted_prices": predictions.tolist()})


@app.route("/recent_predictions", methods=["GET"])
def recent_predictions() -> list:
    """
    Returns last 10 predictions from the database

    Returns:
        list: last 10 predictions
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

    except Exception as error:
        return json.dumps({"error": str(error)}), 400


if __name__ == "__main__":
    app.run()
