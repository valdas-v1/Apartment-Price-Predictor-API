import pandas as pd
from sklearn import preprocessing
import json

pd.options.mode.chained_assignment = None


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

    def change_numeric_type(self) -> None:
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

    def rename_rare(self) -> None:
        """Renames rare categorical values to 'None' to simplify predictions and deal with new unseen values"""
        for col in self.categorical_columns:
            self.df[f"{col} count"] = self.df[col].apply(
                lambda x: (self.df[col] == x).sum()
            )
            self.df[col][self.df[f"{col} count"] < 5] = "None"
            self.df = self.df.drop(f"{col} count", axis=1)

    def create_labelencoder_dict(self) -> None:
        """Creates a LabelEncoder object and encodes the categorical columns"""

        # Adding an extra row with only 'None' values to be able to later encode them despite not having them in the original dataset
        none_val = self.df[self.categorical_columns].iloc[0]
        none_val[self.categorical_columns] = "None"
        self.categorical_values = self.categorical_values.append(none_val)

        self.label_object = {}

        # Iterates though each column creating a new label encoder and encoding the values
        for col in self.categorical_columns:
            labelencoder = preprocessing.LabelEncoder()
            labelencoder.fit(self.categorical_values[col])
            self.categorical_values[col] = labelencoder.fit_transform(
                self.categorical_values[col]
            )
            self.label_object[col] = labelencoder

        # Removing the extra 'None' row
        self.categorical_values = self.categorical_values.iloc[:-1]

    def join_encoded(self) -> None:
        """Joins the encoded numerical and categorical data into a final DataFrame"""
        self.encoded_df = self.encoded_df.join(self.categorical_values)

    def encode(self, le: dict) -> None:
        """Encodes DataFrame with an existing LabelEncoder dictionary or replaces unseen value with 'None'

        Args:
            le (dict): LabelEncoder dictionary
        """
        for col in self.categorical_columns:
            try:
                self.categorical_values[col] = le[col].transform(
                    self.categorical_values[col]
                )
            # Triggers if trying to encode an unseen value
            except ValueError:
                self.categorical_values[col] = "None"

                self.categorical_values[col] = le[col].transform(
                    self.categorical_values[col]
                )
            except Exception:
                return json.dumps({"error": 'Encoder error'}), 500
