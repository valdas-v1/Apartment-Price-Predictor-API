import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import pickle

df = pd.read_csv("250.csv")
df = df.drop_duplicates().reset_index()

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

encoded_df = encoded_df.join(categorical_values)


X_train, X_test, y_train, y_test = train_test_split(encoded_df, df['price'], test_size=0.1)
clf = GradientBoostingRegressor()
clf.fit(X_train, y_train)

# Saving the model and testing data to separate files
pickle.dump(clf, open("house_price_predictor.pkl", "wb"))
pickle.dump(X_test, open("test_data.pkl", "wb"))
pickle.dump(y_test, open("test_labels.pkl", "wb"))
pickle.dump(le, open("label_encoder.pkl", "wb"))