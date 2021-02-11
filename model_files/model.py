import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import pickle
from utils import Encoder

# Load the aparment data from scraping aruodas.lt
df = pd.read_csv("scraping_data/250.csv")
df = df.drop_duplicates().reset_index()

# Creating an Encoder object with the data
encoder = Encoder(df)

# Changing data type of numerical data
encoder.change_numeric_type()

# Renaming rare categorical values to simplify predictions and deal with new unseen values
encoder.rename_rare()

# Creating a LabelEncoder object for all columns
encoder.create_labelencoder_dict()

# Joining encoded numerical and categorical data
encoder.join_encoded()

# Training a Gradient Boosting Regressor model
clf = GradientBoostingRegressor()
clf.fit(encoder.encoded_df, encoder.df["price"])

# Saving the model to a file
with open("house_price_predictor.pkl", "wb") as f:
    pickle.dump(clf, f)

# Saving LabelEncoder object for input encoding and output decoding
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(encoder.label_object, f)
