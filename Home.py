import streamlit as st
import pandas as pd
import numpy as np
import joblib
from PIL import Image


# Load model & encoders
model = joblib.load("model.joblib")
feature_encoders = joblib.load("feature_encoders.joblib")
target_encoders = joblib.load("target_encoders.joblib")

# to get the amount for given acres
FERTILIZER_RANGES = {
    "wheat": {
        "N": {"low": (0, 10), "medium": (15, 20), "high": (25, 30)},
        "P": {"low": (0, 5), "medium": (8, 12), "high": (15, 20)},
        "K": {"low": (0, 5), "medium": (8, 12)}
    },
    "rice": {
        "N": {"low": (0, 10), "medium": (15, 20), "high": (25, 30)},
        "P": {"low": (0, 5), "medium": (8, 12), "high": (15, 20)},
        "K": {"low": (0, 5), "medium": (8, 12)}
    }
}

def compute_fertilizer_quantity(crop, nutrient, level, area):
    min_kg, max_kg = FERTILIZER_RANGES[crop][nutrient][level]
    return {
        "per_acre": f"{min_kg}–{max_kg} kg/acre",
        "total": f"{min_kg * area:.1f}–{max_kg * area:.1f} kg"
    }

#growth stage logic
def get_wheat_stage(days):
    if days <= 25:
        return "early"
    elif days <= 60:
        return "mid"
    else:
        return "late"

def get_rice_stage(days):
    if days <= 20:
        return "early"
    elif days <= 50:
        return "mid"
    else:
        return "late"

#page config
st.set_page_config(
    page_title="Fertilizer Recommendation System",
    layout="centered"
)

st.title("🌾 Fertilizer Recommendation System")
st.subheader("Punjab • Wheat & Rice")

#sidebar
img = Image.open("icon.avif")
st.sidebar.image(img)

st.sidebar.markdown("**Focus:** Wheat & Rice (Punjab)")
st.sidebar.markdown("---")
st.sidebar.markdown("Advisory tool • No soil test required")

#inputs
crop = st.selectbox("Crop", ["Wheat", "Rice"])

days = st.number_input(
    "Days since sowing" if crop == "Wheat" else "Days since transplanting",
    min_value=0,
    max_value=200,
    value=30
)

soil_type = st.selectbox("Soil type", ["Sandy", "Loamy", "Clay"])

prev_n = st.selectbox("Previous Nitrogen level", ["None", "Low", "Medium", "High"])
prev_p = st.selectbox("Previous Phosphorus level", ["None", "Low", "Medium", "High"])
prev_k = st.selectbox("Previous Potassium level", ["None", "Low", "Medium", "High"])

time_since_fert = st.selectbox(
    "Time since last fertilizer application",
    ["<15", "15-30", ">30"]
)

st.markdown("### Irrigation Information")

if crop == "Wheat":
    irrigation_count = st.number_input(
        "Number of irrigations since sowing",
        min_value=0,
        max_value=10,
        value=1
    )
else:
    irrigation_count = np.nan  # not applicable for rice

time_since_irrigation = st.selectbox(
    "Time since last irrigation",
    ["<7", "7-20", ">20"]
)

irrigation_level = st.selectbox(
    "Level of last irrigation",
    ["Light", "Normal", "Heavy"]
)

area = st.number_input(
    "Field area (acres)",
    min_value=0.1,
    max_value=50.0,
    value=1.0
)

# now we will make the code to start prediction
if st.button("Get Fertilizer Recommendation"):

    # Growth stage
    if crop == "Wheat":
        growth_stage = get_wheat_stage(days)
    else:
        growth_stage = get_rice_stage(days)

    
    input_df = pd.DataFrame([{
        "crop": crop.lower(),
        "days_since_start": days,
        "growth_stage": growth_stage,
        "soil_type": soil_type.lower(),
        "prev_N": prev_n.lower(),
        "prev_P": prev_p.lower(),
        "prev_K": prev_k.lower(),
        "time_since_last_fertilizer": time_since_fert,
        "irrigation_count": irrigation_count,
        "time_since_last_irrigation": time_since_irrigation,
        "last_irrigation_level": irrigation_level.lower(),
        "area_acres": area
    }])

    # Handle NaN irrigation count only for (rice)
    input_df["irrigation_count"] = input_df["irrigation_count"].fillna(-1)

    # Encode features
    for col, encoder in feature_encoders.items():
        input_df[col] = encoder.transform(input_df[col].astype(str))

    # Predict
    prediction = model.predict(input_df)[0]

    # Decode outputs
    N = target_encoders["N_class"].inverse_transform([prediction[0]])[0]
    P = target_encoders["P_class"].inverse_transform([prediction[1]])[0]
    K = target_encoders["K_class"].inverse_transform([prediction[2]])[0]

    crop_key = crop.lower()

    N_qty = compute_fertilizer_quantity(crop_key, "N", N, area)
    P_qty = compute_fertilizer_quantity(crop_key, "P", P, area)
    K_qty = compute_fertilizer_quantity(crop_key, "K", K, area)

    # output 
    st.success("✅ Fertilizer Recommendation Generated")

    st.markdown("### 🧪 Nutrient Requirement & Quantity")

    st.write({
        "Nitrogen (N)": {
            "Requirement": N.upper(),
            "Per acre": N_qty["per_acre"],
            "Total for field": N_qty["total"]
        },
        "Phosphorus (P)": {
            "Requirement": P.upper(),
            "Per acre": P_qty["per_acre"],
            "Total for field": P_qty["total"]
        },
        "Potassium (K)": {
            "Requirement": K.upper(),
            "Per acre": K_qty["per_acre"],
            "Total for field": K_qty["total"]
        }
    })

    st.info(
        "This is an advisory recommendation based on crop stage, soil type, "
        "and field history. Soil testing is recommended for precision."
    )
