import pandas as pd
from sklearn import preprocessing
import pickle

class Encoder:
    def __init__(self, df):
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

        self.encoded_df = pd.DataFrame()

        self.categorical_values = self.df[
            [
                "Building type",
                "Equipment",
                "Heating system",
                "city",
                "region",
                "street",
            ]
        ]

    def change_numeric_type(self):
        self.df = self.df.astype(
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

        self.encoded_df[self.numerical_columns] = self.df[self.numerical_columns]

    def create_labelencoder_dict(self):
        self.label_object = {}
        for col in self.categorical_columns:
            labelencoder = preprocessing.LabelEncoder()
            labelencoder.fit(self.categorical_values[col])
            self.categorical_values[col] = labelencoder.fit_transform(
                self.categorical_values[col]
            )
            self.label_object[col] = labelencoder

    def join_encoded(self):
        self.encoded_df = self.encoded_df.join(self.categorical_values)
