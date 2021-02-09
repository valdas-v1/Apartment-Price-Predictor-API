import pandas as pd
from sklearn import preprocessing
import json


class Encoder:
    """Encoder class with methods to encode new values or with an existing LabelEncoder dictionary"""

    def __init__(self, df: pd.DataFrame):
        # Placeholder DataFrame to hold working DataFrame
        self.df = df

        self.categorical_columns = [
            "Building type",
            "Equipment",
            "Heating system",
            "city",
            "region",
            "street",
        ]

        self.numerical_columns = [
            "Area",
            "Build year",
            "Floor",
            "No. of floors",
            "Number of rooms",
            "Renovation year",
        ]

        # Placeholder DataFrame to hold encoded data
        self.encoded_df = pd.DataFrame()

        self.categorical_values = self.df[self.categorical_columns]

    def change_numeric_type(self):
        """Changes the type of numerical values to numerical data types"""
        self.df = self.df.astype(
            {
                "Area": "float64",
                "Build year": "int64",
                "Floor": "int64",
                "No. of floors": "int64",
                "Renovation year": "int64",
                "Number of rooms": "int64",
            }
        )

        if "price" in self.df.columns:
            self.df = self.df.astype({"price": "float64"})

        self.encoded_df[self.numerical_columns] = self.df[self.numerical_columns]

    def create_labelencoder_dict(self):
        """Creates a LabelEncoder object and encodes the categorical columns"""
        self.label_object = {}

        # Iterates though each column creating a new label encoder and encoding the values
        for col in self.categorical_columns:
            labelencoder = preprocessing.LabelEncoder()
            labelencoder.fit(self.categorical_values[col])
            self.categorical_values[col] = labelencoder.fit_transform(
                self.categorical_values[col]
            )
            self.label_object[col] = labelencoder

    def join_encoded(self):
        """Joins the encoded numerical and categorical data into a final DataFrame"""
        self.encoded_df = self.encoded_df.join(self.categorical_values)

    def encode(self, le: dict):
        """Encodes DataFrame with an existing LabelEncoder dictionary

        Args:
            le (dict): LabelEncoder dictionary
        """
        try:
            for col in self.categorical_columns:
                self.categorical_values[col] = le[col].transform(
                    self.categorical_values[col]
                )
        except Exception as error:
            return json.dumps({"error": str(error)}), 400
