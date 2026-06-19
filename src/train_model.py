import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load cleaned dataset
df = pd.read_csv("data/cleaned_ddos.csv")

# Convert labels
df["Label"] = df["Label"].map({
    "BENIGN": 0,
    "DDoS": 1
})

# Separate features and target
X = df.drop("Label", axis=1)
y = df["Label"]

# Keep only numeric columns
X = X.select_dtypes(include=["number"])

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# Train Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))