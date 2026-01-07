import pandas as pd

# 1️⃣ Load your file
df = pd.read_csv("sustainable_products_2000_with_links.csv")

# 2️⃣ Category → Image mapping
category_images = {
    "Electronics": "https://via.placeholder.com/500x400?text=Electronics+Product",
    "Household": "https://via.placeholder.com/500x400?text=Household+Product",
    "Fashion": "https://via.placeholder.com/500x400?text=Fashion+Product",
    "Kitchen": "https://via.placeholder.com/500x400?text=Kitchen+Product",
    "Personal Care": "https://via.placeholder.com/500x400?text=Personal+Care",
    "Stationery": "https://via.placeholder.com/500x400?text=Stationery",
    "Bags": "https://via.placeholder.com/500x400?text=Bags",
}

# 3️⃣ Add Image column if missing
if "Image_URL" not in df.columns:
    df["Image_URL"] = ""

# 4️⃣ Fill blank Image_URL values based on category
df["Image_URL"] = df.apply(
    lambda row: category_images.get(row["Category"], "https://via.placeholder.com/500x400?text=Product")
    if row["Image_URL"] == "" else row["Image_URL"],
    axis=1
)

# 5️⃣ Save updated file
output_file = "updated_sustainable_products_with_images.csv"
df.to_csv(output_file, index=False)

print("File created:", output_file)
