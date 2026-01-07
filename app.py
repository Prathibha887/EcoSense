from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import joblib
import numpy as np
import urllib.parse

app = Flask(__name__)

CSV_PATH = "generated_sustainable_products_1110.csv"
MODEL_PATH = "sustainability_model.pkl"
ENCODER_PATH = "label_encoder.pkl"

# -------------------- LOAD DATA --------------------
df = pd.read_csv(CSV_PATH)
df.reset_index(inplace=True)

# -------------------- LOAD MODEL --------------------
try:
    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)
except:
    model = None
    encoder = None

FEATURE_COLS = [
    "Recyclability_pct",
    "Carbon_kgCO2",
    "Biodegradability",
    "Lifespan_years"
]

# -------------------- ECO SCORE --------------------
max_life = df["Lifespan_years"].replace(0, np.nan).max()
if pd.isna(max_life) or max_life == 0:
    max_life = 1.0

def compute_eco_score(row):
    return (
        0.35 * (row["Recyclability_pct"] / 100) +
        0.20 * (row["Biodegradability"] / 100) +
        0.30 * (1 / (1 + row["Carbon_kgCO2"])) +
        0.15 * (row["Lifespan_years"] / max_life)
    )

df["eco_score"] = df.apply(compute_eco_score, axis=1)

# -------------------- HELPERS --------------------

# Rank materials BEST → WORST
def rank_materials(category):
    cat_df = df[df["Category"].str.lower() == category.lower()].copy()
    if cat_df.empty:
        return []

    return (
        cat_df.groupby("Material")["eco_score"]
        .mean()
        .sort_values(ascending=False)
        .index.tolist()
    )

def get_product(category, material):
    return df[
        (df["Category"].str.lower() == category.lower()) &
        (df["Material"] == material)
    ].iloc[0].to_dict()

def generate_buy_link(product):
    query = f"{product['Material']} {product['Category']}"
    encoded_query = urllib.parse.quote_plus(query)
    return f"https://www.amazon.in/s?k={encoded_query}"

# -------------------- ROUTES --------------------

@app.route("/")
def home():
    return render_template("index.html")

# -------- SEARCH → START FROM BEST --------
@app.route("/search", methods=["POST"])
def search():
    category = request.form.get("product", "").strip()
    materials = rank_materials(category)

    if not materials:
        return render_template("search_results.html", error="Category not found.")

    best_product = get_product(category, materials[0])
    return redirect(url_for("product_page", pid=best_product["index"]))

# -------- PRODUCT PAGE: BEST → WORST --------
@app.route("/product/<int:pid>")
def product_page(pid):

    if pid not in df["index"].values:
        return "Product not found", 404

    product = df[df["index"] == pid].iloc[0].to_dict()

    # ML Prediction
    if model:
        X = df.loc[df["index"] == pid, FEATURE_COLS]
        pred = model.predict(X)[0]
        predicted_label = encoder.inverse_transform([pred])[0]
    else:
        predicted_label = product["Label"]

    category = product["Category"]
    material = product["Material"]

    materials = rank_materials(category)
    current_pos = materials.index(material)

    # Check if BEST product
    is_best = current_pos == 0

    buy_link = None
    if is_best:
        buy_link = generate_buy_link(product)

    # Next WORSE product
    alternative = None
    alternative_exists = False

    if current_pos + 1 < len(materials):
        next_material = materials[current_pos + 1]
        alternative = get_product(category, next_material)
        alternative_exists = True

    return render_template(
        "product_details.html",
        product=product,
        predicted_label=predicted_label,
        alternative=alternative,
        alternative_exists=alternative_exists,
        buy_link=buy_link,
        is_best=is_best
    )

# -------------------- CATEGORY BROWSER --------------------
@app.route("/categories")
def categories():
    categories = sorted(df["Category"].unique())
    return render_template("category_browser.html", categories=categories)

@app.route("/category/<name>")
def open_category(name):
    materials = rank_materials(name)
    if not materials:
        return "Category not found", 404

    best_product = get_product(name, materials[0])
    return redirect(url_for("product_page", pid=best_product["index"]))

# -------------------- COMPARE PAGE --------------------
@app.route("/compare", methods=["GET", "POST"])
def compare():
    categories = sorted(df["Category"].unique())
    bestA = bestB = None
    selectedA = selectedB = None

    if request.method == "POST":
        selectedA = request.form.get("catA")
        selectedB = request.form.get("catB")

        if selectedA == selectedB:
            return render_template(
                "comparison.html",
                categories=categories,
                error="Select two different categories."
            )

        matA = rank_materials(selectedA)
        matB = rank_materials(selectedB)

        bestA = get_product(selectedA, matA[0])
        bestB = get_product(selectedB, matB[0])

    return render_template(
        "comparison.html",
        categories=categories,
        bestA=bestA,
        bestB=bestB,
        selectedA=selectedA,
        selectedB=selectedB
    )

# -------------------- COUNTRIES --------------------
@app.route("/countries")
def countries():
    countries_data = [
        {"name": "Finland", "rank": 1, "highlights": "Renewable energy, clean air"},
        {"name": "Sweden", "rank": 2, "highlights": "Recycling & green transport"},
        {"name": "Denmark", "rank": 3, "highlights": "Wind energy leader"},
        {"name": "Germany", "rank": 4, "highlights": "Waste management"},
        {"name": "Netherlands", "rank": 5, "highlights": "Sustainable cities"},
        {"name": "Norway", "rank": 6, "highlights": "Hydropower"},
        {"name": "Switzerland", "rank": 7, "highlights": "Environmental policy"},
        {"name": "Austria", "rank": 8, "highlights": "Forest sustainability"},
        {"name": "UK", "rank": 9, "highlights": "Carbon reduction"},
        {"name": "Japan", "rank": 10, "highlights": "Energy efficiency"}
    ]
    return render_template("countries.html", countries=countries_data)

# -------------------- AWARENESS --------------------
@app.route("/awareness")
def awareness():
    return render_template("awareness.html")

@app.route("/check", methods=["GET", "POST"])
def check():

    result = None

    if request.method == "POST":
        # Read user input
        recyclability = float(request.form["recyclability"])
        carbon = float(request.form["carbon"])
        biodegradability = float(request.form["biodegradability"])
        lifespan = float(request.form["lifespan"])

        # Normalize lifespan using same max_life logic
        life_norm = lifespan / max_life

        # Calculate eco score (same formula as dataset)
        eco_score = (
            0.35 * (recyclability / 100) +
            0.20 * (biodegradability / 100) +
            0.30 * (1 / (1 + carbon)) +
            0.15 * life_norm
        )

        # Decide label based on score
        if eco_score >= 0.65:
            result = "Eco-Friendly"
        elif eco_score >= 0.40:
            result = "Moderately Sustainable"
        else:
            result = "Not Sustainable"

    return render_template("check_sustainability.html", result=result)

# -------------------- RUN --------------------
if __name__ == "__main__":
    app.run(debug=True)
