import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

df = pd.read_csv("data/cleaned_ddos.csv")

df["Label"] = df["Label"].map({
    "BENIGN": 0,
    "DDoS": 1
})

X = df.drop("Label", axis=1)
X = X.select_dtypes(include=["number"])

y = df["Label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["BENIGN", "DDoS"]
)

disp.plot()

plt.savefig(
    "screenshots/confusion_matrix.png"
)

print("Confusion Matrix Saved!")