import pandas as pd
import random

#levels are: 
LEVELS = ["LOW", "MEDIUM", "HIGH"]

def clamp_level(level):

    return LEVELS[max(0, min(2, level))]

def level_to_index(level):
    return LEVELS.index(level)

def index_to_level(idx):
    return clamp_level(idx)

# -------------------------------
# Growth stage logic
# -------------------------------
def get_growth_stage(days):
    if days <= 25:
        return "EARLY"
    elif days <= 60:
        return "MID"
    else:
        return "LATE"

# -------------------------------
# Base requirement by stage
# -------------------------------
BASE_REQUIREMENT = {
    "EARLY": {"N": "HIGH", "P": "MEDIUM", "K": "LOW"},
    "MID":   {"N": "HIGH", "P": "LOW",    "K": "LOW"},
    "LATE":  {"N": "LOW",  "P": "LOW",    "K": "LOW"},
}

# -------------------------------
# Adjustment functions
# -------------------------------
def adjust_by_previous(level, prev_level):
    idx = level_to_index(level)
    if prev_level == "NONE":
        idx += 1
    elif prev_level == "HIGH":
        idx -= 1
    return index_to_level(idx)

def adjust_by_soil_n(level, soil):
    idx = level_to_index(level)
    if soil == "SANDY":
        idx += 1
    elif soil == "CLAY":
        idx -= 1
    return index_to_level(idx)

def adjust_by_irrigation_n(level, irrigations):
    idx = level_to_index(level)
    if irrigations >= 2:
        idx += 1
    return index_to_level(idx)

def adjust_by_time_n(level, time_bucket):
    idx = level_to_index(level)
    if time_bucket == "<15":
        idx -= 1
    elif time_bucket == ">30":
        idx += 1
    return index_to_level(idx)

def potassium_safety(level):
    # Potassium should never be HIGH for wheat
    if level == "HIGH":
        return "MEDIUM"
    return level

# -------------------------------
# Single row generator
# -------------------------------
def generate_wheat_row():
    days = random.randint(5, 120)
    stage = get_growth_stage(days)

    soil = random.choice(["SANDY", "LOAMY", "CLAY"])

    prev_N = random.choice(["NONE", "LOW", "MEDIUM", "HIGH"])
    prev_P = random.choice(["NONE", "LOW", "MEDIUM", "HIGH"])
    prev_K = random.choice(["NONE", "LOW", "MEDIUM", "HIGH"])

    irrigations = random.randint(0, 4)
    time_since = random.choice(["<15", "15-30", ">30"])
    area = round(random.uniform(0.5, 5.0), 2)

    # Base
    N = BASE_REQUIREMENT[stage]["N"]
    P = BASE_REQUIREMENT[stage]["P"]
    K = BASE_REQUIREMENT[stage]["K"]

    # Previous fertilizer adjustment
    N = adjust_by_previous(N, prev_N)
    P = adjust_by_previous(P, prev_P)
    K = adjust_by_previous(K, prev_K)

    # Soil adjustment (Nitrogen only)
    N = adjust_by_soil_n(N, soil)

    # Irrigation adjustment (Nitrogen only)
    N = adjust_by_irrigation_n(N, irrigations)

    # Time since last fertilizer (Nitrogen mainly)
    N = adjust_by_time_n(N, time_since)

    # Potassium safety rule
    K = potassium_safety(K)

    return {
        "Crop": "WHEAT",
        "Days_Since_Sowing": days,
        "Growth_Stage": stage,
        "Soil_Type": soil,
        "Prev_N_Level": prev_N,
        "Prev_P_Level": prev_P,
        "Prev_K_Level": prev_K,
        "Irrigation_Count": irrigations,
        "Time_Since_Last_Fertilizer": time_since,
        "Area_Acres": area,
        "N_Class": N,
        "P_Class": P,
        "K_Class": K
    }

# -------------------------------
# Generate dataset
# -------------------------------
def generate_dataset(n_rows=3000):
    data = [generate_wheat_row() for _ in range(n_rows)]
    return pd.DataFrame(data)

# -------------------------------
# Run generation
# -------------------------------
if __name__ == "__main__":
    df = generate_dataset(3000)
    df.to_csv("wheat_fertilizer_dataset.csv", index=False)
    print("Dataset generated:", df.shape)
    print(df.head())
