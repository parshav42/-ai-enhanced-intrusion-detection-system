import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/cleaned_ddos.csv")

df["Label"].value_counts().plot(kind="bar")

plt.title("Attack Distribution")
plt.xlabel("Class")
plt.ylabel("Count")

plt.savefig("screenshots/attack_distribution.png")
print("Graph saved successfully!")