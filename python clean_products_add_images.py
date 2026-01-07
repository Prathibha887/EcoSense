import pandas as pd
import random

# Categories and materials with base values
categories = {
    "Water Bottle": [
        ("Plastic", 20, 150, 5, 3),
        ("Stainless Steel", 90, 20, 15, 10),
        ("Copper", 85, 25, 10, 9),
        ("Glass", 95, 15, 20, 7),
        ("Bamboo", 98, 10, 90, 5)
    ],
    "Toothbrush": [
        ("Plastic", 10, 80, 2, 1),
        ("Bamboo", 95, 10, 95, 1),
        ("Charcoal", 70, 30, 35, 1),
        ("Recycled Plastic", 60, 40, 20, 1)
    ],
    "Cleaning Brush": [
        ("Plastic", 15, 120, 5, 3),
        ("Coconut Fiber", 98, 10, 98, 2),
        ("Wooden", 90, 15, 80, 4)
    ],
    "Hair Brush": [
        ("Plastic", 20, 100, 3, 3),
        ("Wooden", 90, 20, 70, 5),
        ("Bamboo", 95, 15, 85, 5)
    ],
    "Clothing": [
        ("Cotton", 80, 40, 90, 2),
        ("Polyester", 5, 120, 0, 5),
        ("Organic Cotton", 95, 25, 95, 3),
        ("Recycled Fabric", 70, 35, 80, 4),
        ("Nylon", 10, 140, 0, 6)
    ],
    "Kitchen Item": [
        ("Plastic", 15, 130, 2, 5),
        ("Steel", 90, 25, 20, 20),
        ("Glass", 95, 20, 30, 10),
        ("Silicone", 70, 40, 80, 8)
    ],
    "Household": [
        ("Plastic", 10, 150, 2, 7),
        ("Steel", 85, 30, 10, 15),
        ("Bamboo", 95, 10, 95, 5)
    ],
    "Bags": [
        ("Cotton", 85, 25, 95, 4),
        ("Jute", 95, 20, 95, 4),
        ("Nylon", 5, 150, 0, 6),
        ("Recycled Plastic", 60, 45, 25, 6)
    ]
}

rows = []

# Generate 2000 rows
for _ in range(2000):
    category = random.choice(list(categories.keys()))
    material, rec, carbon, bio, life = random.choice(categories[category])

    # Add slight variation
    rec_v = max(0, min(100, rec + random.uniform(-4, 4)))
    carbon_v = max(1, carbon + random.uniform(-4, 4))
    bio_v = max(0, min(100, bio + random.uniform(-4, 4)))
    life_v = max(1, life + random.uniform(-0.5, 0.5))

    # Decide sustainability label
    if rec_v >= 80 and carbon_v <= 40:
        label = "Eco-Friendly"
    elif rec_v >= 40 or carbon_v <= 80:
        label = "Moderate"
    else:
        label = "Not Sustainable"

    # Auto-generate image based on category
    image_url = f"https://via.placeholder.com/500x400?text={category.replace(' ', '+')}"

    product_link = "https://www.amazon.in"

    rows.append([
        category, material, rec_v, carbon_v, bio_v, life_v,
        image_url, product_link, label
    ])

# Convert to DataFrame
df = pd.DataFrame(rows, columns=[
    "Category", "Material", "Recyclability_pct", "Carbon_kgCO2",
    "Biodegradability", "Lifespan_years", "Image_URL",
    "Product_Link", "Label"
])

# Save locally
df.to_csv("clean_sustainable_2000.csv", index=False)

print("File saved successfully as clean_sustainable_2000.csv")
