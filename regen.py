import pandas as pd
import random

# Load dataset
df = pd.read_csv("generated_sustainable_products_1110.csv")

# Add Variant column
variant_pool = [
    "Standard",
    "Recycled",
    "Low-Grade",
    "Premium",
    "Coated",
    "Untreated"
]

df["Variant"] = df.apply(
    lambda x: random.choice(variant_pool),
    axis=1
)

# 🔀 SHUFFLE DATASET (IMPORTANT)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save back to CSV
df.to_csv("generated_sustainable_products_1110.csv", index=False)

print("Variant column added and dataset shuffled successfully")
