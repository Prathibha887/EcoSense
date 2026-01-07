import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("sustainable_products_2000_with_links.csv")

X = df[["Recyclability_pct","Carbon_kgCO2","Biodegradability","Lifespan_years"]]
y = df["Label"]

encoder = LabelEncoder()
y_enc = encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "sustainability_model.pkl")
joblib.dump(encoder, "label_encoder.pkl")

print("Model training completed. Files saved successfully.")
