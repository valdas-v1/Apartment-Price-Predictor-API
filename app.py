import pickle
import json
from flask import Flask, request
import numpy as np
import pandas as pd
from database import Database

SAVED_MODEL_PATH = "model_files/house_price_predictor.pkl"
SAVED_LABEL_ENCODER_PATH = "model_files/label_encoder.pkl"

# Loading the classifier and label encoder from file
classifier = pickle.load(open(SAVED_MODEL_PATH, "rb"))
le = pickle.load(open(SAVED_LABEL_ENCODER_PATH, "rb"))

app = Flask(__name__)
db = Database()


def __process_input(request_data: list) -> pd.DataFrame:
    """
    Transforms the provided JSON to a Pandas DataFrame
    """
    return pd.DataFrame.from_dict(json.loads(request.data)["inputs"])


def __encode_input(data: pd.DataFrame) -> pd.DataFrame:
    data = data.astype(
        {
            "Area": "float64",
            "Build year": "int64",
            "Floor": "int64",
            "No. of floors": "int64",
            "Renovation year": "int64",
            "price": "float64",
            "Number of rooms": "int64",
        }
    )

    # Categorical data to be encoded
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

    # Encoding categorical data with Scikit-Learn LabelEncoder
    le = preprocessing.LabelEncoder()
    categorical_values = data[
        [
            "Building type",
            "Equipment",
            "Heating system",
            "city",
            "region",
            "street",
        ]
    ].apply(le.fit_transform)

    # Joining and returning encoded numerical and categorical data
    return encoded_data.join(categorical_values)


@app.route("/predict", methods=["POST"])
def predict() -> list:
    """
    Takes encoded data about a house and makes a price prediction with a pretrained model.
    Can accept as many house inputs as provided
    """
    input_params = __process_input(request.data)
    try:
        predictions = classifier.predict(input_params)
    except Exception as error:
        return json.dumps({"error": str(error)}), 400

    # Add prediction to database
    prediction_data = input_params
    prediction_data["predicted price"] = predictions
    db.push_dataframe_to_db("predictions", prediction_data)

    return json.dumps({"predicted_prices": predictions.tolist()})


@app.route("/predict_raw", methods=["POST"])
def predict_raw() -> list:
    """
    Takes encoded data about a house and makes a price prediction with a pretrained model.
    Can accept as many house inputs as provided
    """
    input_params = __encode_input(__process_input(request.data))
    try:
        predictions = classifier.predict(input_params)
    except Exception as error:
        return json.dumps({"error": str(error)}), 400

    # Add prediction to database
    prediction_data = input_params
    prediction_data["predicted price"] = predictions
    db.push_dataframe_to_db("predictions", prediction_data)

    return json.dumps({"predicted_prices": predictions.tolist()})


if __name__ == "__main__":
    app.run(debug=True)
