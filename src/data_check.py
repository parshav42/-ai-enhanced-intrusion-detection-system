import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv(
    "data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
)

print("Original Shape:", df.shape)

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Replace infinity values
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Remove missing values
df.dropna(inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

print("Cleaned Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nAttack Distribution:")
print(df["Label"].value_counts())

df.to_csv(
    "data/cleaned_ddos.csv",
    index=False
)

print("Cleaned dataset saved.")