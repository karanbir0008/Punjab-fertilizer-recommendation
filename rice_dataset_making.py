import pandas as pd
import random

# levels
levels = ["low", "medium", "high"]

def get_int_level(level):
    return levels.index(level)

def get_str_level(idx):
    idx = max(0, min(2, idx))
    return levels[idx]


# Soil affects N only
def soil_level_relation(level, soil_type):
    idx = get_int_level(level)
    soil_type = soil_type.lower()

    if soil_type == "sandy":
        idx += 1
    elif soil_type == "clay":
        idx -= 1

    return get_str_level(idx)

# Previous fertilizer effect
def prev_fertilizer_level_relation(level, prev_level):
    idx = get_int_level(level)
    prev_level = prev_level.lower()

    if prev_level == "none":
        idx += 1
    elif prev_level == "high":
        idx -= 1

    return get_str_level(idx)

# Time since last fertilizer
def prev_fertilization_time_level_relation(level, time_bucket):
    idx = get_int_level(level)

    if time_bucket == "<15":
        idx -= 1
    elif time_bucket == ">30":
        idx += 1

    return get_str_level(idx)

# Irrigation recency + intensity (N only, capped)
def irrigation_recency_and_level_relation(time_bucket, irr_level, level):
    idx = get_int_level(level)
    adjustment = 0

    if time_bucket == "<7":
        adjustment += 1

    if irr_level.lower() == "heavy":
        adjustment += 1

    adjustment = min(1, adjustment)  
    idx += adjustment

    return get_str_level(idx)

# Potassium safety (never HIGH)
def potassium_safety(level):
    if level == "high":
        return "medium"
    return level

# base requirement
rice_stage_base = {
    "early": {"N": "high",   "P": "medium", "K": "low"},
    "mid":   {"N": "medium", "P": "low",    "K": "low"},
    "late":  {"N": "low",    "P": "low",    "K": "low"}
}

def get_rice_stage(days):
    if days <= 20:
        return "early"
    elif days <= 50:
        return "mid"
    else:
        return "late"

#generating one row of data
def generate_rice_row():
    days = random.randint(5, 120)
    soil_type = random.choice(["sandy", "loamy", "clay"])

    prev_n = random.choice(["none", "low", "medium", "high"])
    prev_p = random.choice(["none", "low", "medium", "high"])
    prev_k = random.choice(["none", "low", "medium", "high"])

    time_since_fert = random.choice(["<15", "15-30", ">30"])
    time_since_irr = random.choice(["<7", "7-20", ">20"])
    irr_level = random.choice(["light", "normal", "heavy"])

    area = round(random.uniform(0.5, 5.0), 2)

    stage = get_rice_stage(days)

    # Base levels
    N = rice_stage_base[stage]["N"]
    P = rice_stage_base[stage]["P"]
    K = rice_stage_base[stage]["K"]

    # Nitrogen 
    N = prev_fertilizer_level_relation(N, prev_n)
    N = soil_level_relation(N, soil_type)
    N = prev_fertilization_time_level_relation(N, time_since_fert)
    N = irrigation_recency_and_level_relation(time_since_irr, irr_level, N)

    # Phosphorus 
    P = prev_fertilizer_level_relation(P, prev_p)
    P = prev_fertilization_time_level_relation(P, time_since_fert)

    # Potassium 
    K = prev_fertilizer_level_relation(K, prev_k)
    K = prev_fertilization_time_level_relation(K, time_since_fert)
    K = potassium_safety(K)

    return {
        "crop": "rice",
        "days_since_transplanting": days,
        "growth_stage": stage,
        "soil_type": soil_type,
        "prev_N": prev_n,
        "prev_P": prev_p,
        "prev_K": prev_k,
        "time_since_last_fertilizer": time_since_fert,
        "time_since_last_irrigation": time_since_irr,
        "last_irrigation_level": irr_level,
        "area_acres": area,
        "N_class": N,
        "P_class": P,
        "K_class": K
    }


def generate_rice_dataset(n_rows=3000):
    rows = []
    for _ in range(n_rows):
        rows.append(generate_rice_row())
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = generate_rice_dataset(3000)
    df.to_csv("rice_fertilizer_dataset.csv", index=False)

    print("Rice dataset generated successfully")
    print(df.head())
