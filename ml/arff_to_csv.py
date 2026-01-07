from scipy.io import arff
import pandas as pd

data, meta = arff.loadarff("Training Dataset.arff")
df = pd.DataFrame(data)

# Convert byte strings to normal strings
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].str.decode("utf-8")

df.to_csv("dataset.csv", index=False)
print("dataset.csv created successfully")
