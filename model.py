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

# Creating a LabelEncoder object for all columns
encoder.create_labelencoder_dict()

# Joining encoded numerical and categorical data
encoder.join_encoded()

# Spliting the data and training a Gradient Boosting Regressor model
X_train, X_test, y_train, y_test = train_test_split(
    encoder.encoded_df, encoder.df["price"], test_size=0.1
)
clf = GradientBoostingRegressor()
clf.fit(X_train, y_train)

# Saving the model and testing data to separate files
with open("model_files/house_price_predictor.pkl", "wb") as f:
    pickle.dump(clf, f)
with open("model_files/test_data.pkl", "wb") as f:
    pickle.dump(X_test, f)
with open("model_files/test_labels.pkl", "wb") as f:
    pickle.dump(y_test, f)


# Saving LabelEncoder object for input encoding and output decoding
with open("model_files/label_encoder.pkl", "wb") as f:
    pickle.dump(encoder.label_object, f)
