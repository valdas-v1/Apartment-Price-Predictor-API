import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import pickle

# Load the aparment data from scraping aruodas.lt
df = pd.read_csv("scraping_data/250.csv")
df = df.drop_duplicates().reset_index()

# Changing data type of numeric data
df = df.astype(
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
encoded_df = df[
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
categorical_values = df[
    [
        "Building type",
        "Equipment",
        "Heating system",
        "city",
        "region",
        "street",
    ]
].apply(le.fit_transform)

# Joining encoded numerical and categorical data
encoded_df = encoded_df.join(categorical_values)

# Spliting the data and training a Gradient Boosting Regressor model
X_train, X_test, y_train, y_test = train_test_split(
    encoded_df, df["price"], test_size=0.1
)
clf = GradientBoostingRegressor()
clf.fit(X_train, y_train)

# Saving the model and testing data to separate files
pickle.dump(clf, open("model_files/house_price_predictor.pkl", "wb"))
pickle.dump(X_test, open("model_files/test_data.pkl", "wb"))
pickle.dump(y_test, open("model_files/test_labels.pkl", "wb"))

# Saving LabelEncoder object for input encoding and output decoding
pickle.dump(le, open("model_files/label_encoder.pkl", "wb"))
