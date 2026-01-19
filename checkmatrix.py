import pandas as pd 
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import LabelEncoder 

# Load dataset
df = pd.read_csv("Sustainable_products.csv")

# Features and target
X = df[["Recyclability_pct", "Carbon_kgCO2", "Biodegradability", "Lifespan_years"]]
y = df["Label"]

# Encode labels
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import accuracy_score, classification_report 

model = DecisionTreeClassifier(criterion="gini", max_depth=5, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=encoder.classes_))
