import pickle
import json
from flask import Flask, request
import numpy as np
import pandas as pd

SAVED_MODEL_PATH = "model_files/house_price_predictor.pkl"

# Loading the classifier from file
classifier = pickle.load(open(SAVED_MODEL_PATH, "rb"))

app = Flask(__name__)


def __process_input(request_data: list) -> pd.DataFrame:
    """
    Transforms the provided JSON to a Pandas DataFrame
    """
    return pd.DataFrame.from_dict(json.loads(request.data)["inputs"])


@app.route("/predict", methods=["POST"])
def predict() -> list:
    """
    Takes data about a house and makes a price prediction with a pretrained model.
    Can accept as many house inputs as provided
    """
    input_params = __process_input(request.data)
    try:
        predictions = classifier.predict(input_params)
    except Exception as error:
        return json.dumps({"error": str(error)}), 400

    return json.dumps({"predicted_prices": predictions.tolist()})


if __name__ == "__main__":
    app.run(debug=True)
