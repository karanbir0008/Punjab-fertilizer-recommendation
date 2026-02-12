import random
import pandas as pd

#levels are for N,P,K:
levels = ["low","medium","high"]

#to get 0,1,2
def get_int_level(str_level):
    return levels.index(str_level)

#to get the string output
def get_str_level(int_level):
    if int_level ==0 or int_level == 1 or int_level==2:
        return levels[int_level]
    elif int_level>2:
        return levels[2]
    elif int_level<0:
        return levels[0]


'''
1. first factor is time period of sowing.
2. then comes the soil type
3. then comes the previous level of fertilizer
4. then comes time since last fertilization. 
5. then comes the previous irrigation
'''
#to get the time period
def get_sowing_period(days):
    if days <= 25:
        return "early"
    elif days <= 60:
        return "mid"
    else:
        return "late"
    
#mapping the values for N,P,K as per seed sowing
sow_fertilizer_relation = {
    "early":{"N":"high","P":"medium","K":"low"},
    "mid":{"N":"high","P":"low","K":"low"},
    "late":{"N":"low","P":"low","K":"low"}
}

def soil_level_relation(level,soil_type):
    #only nitrogen gets affected by soil type
    idx = get_int_level(level)
    if soil_type.lower() == "sandy":
        idx+=1
    elif soil_type.lower() == "loamy":
        idx+=0
    elif soil_type.lower() == "clay":
        idx-=1
    return get_str_level(idx)

#relation with fertilizers given previously
def prev_fertilizer_level_relation(level,prev_level):
    idx = get_int_level(level)
    if prev_level == "none":
        idx += 1
    elif prev_level == "high":
        idx -= 1
    return get_str_level(idx)

#relation with time since last fertilizer was given
def prev_fertilization_time_level_relation(level,time):
    idx = get_int_level(level)
    if time == "<15":
        idx -= 1
    elif time == ">30":
        idx += 1
    return get_str_level(idx)

#relation with previous irrigations since sowing
def prev_n_irrigations_level_relation(number_of_irr,level):
    idx = get_int_level(level)
    if number_of_irr >= 2:
        idx += 1
    return get_str_level(idx)

def irrigation_recency_and_level_relation(time_bucket, irr_level, level):
    idx = get_int_level(level)
    adjustment = 0

    if time_bucket == "<7":
        adjustment += 1

    if irr_level.lower() == "heavy":
        adjustment += 1

    # cap to +1 to avoid double counting
    adjustment = min(1, adjustment)

    idx += adjustment
    return get_str_level(idx)


#potassium safety
def potassium_safety(level):
    if level == "high":
        return "medium"
    return level


# function to create one row
def generate_wheat_row():
    days = random.randint(5,120)
    soil_type = random.choice(["sandy","loamy","clay"])

    prev_n = random.choice(["none", "low", "medium", "high"])
    prev_p = random.choice(["none", "low", "medium", "high"])
    prev_k = random.choice(["none", "low", "medium", "high"])

    time_since_fert = random.choice(["<15", "15-30", ">30"])

    irr_count = random.randint(0, 4)
    time_since_irr = random.choice(["<7", "7-20", ">20"])
    irr_level = random.choice(["light", "normal", "heavy"])

    area = round(random.uniform(0.5, 5.0), 2)

    #Growth stage 
    stage = get_sowing_period(days)

    #  Base values
    N = sow_fertilizer_relation[stage]["N"]
    P = sow_fertilizer_relation[stage]["P"]
    K = sow_fertilizer_relation[stage]["K"]

    #  Applying rules 

    # Nitrogen
    N = prev_fertilizer_level_relation(N, prev_n)
    N = soil_level_relation(N, soil_type)
    N = prev_n_irrigations_level_relation(irr_count, N)
    N = prev_fertilization_time_level_relation(N, time_since_fert)
    N = irrigation_recency_and_level_relation(time_since_irr, irr_level, N)

    # Phosphorus
    P = prev_fertilizer_level_relation(P, prev_p)
    P = prev_fertilization_time_level_relation(P, time_since_fert)

    # Potassium
    K = prev_fertilizer_level_relation(K, prev_k)
    K = prev_fertilization_time_level_relation(K, time_since_fert)
    K = potassium_safety(K)

    # Final row
    return {
        "crop": "wheat",
        "days_since_sowing": days,
        "growth_stage": stage,
        "soil_type": soil_type,
        "prev_N": prev_n,
        "prev_P": prev_p,
        "prev_K": prev_k,
        "time_since_last_fertilizer": time_since_fert,
        "irrigation_count": irr_count,
        "time_since_last_irrigation": time_since_irr,
        "last_irrigation_level": irr_level,
        "area_acres": area,
        "N_class": N,
        "P_class": P,
        "K_class": K
    }

def generate_wheat_dataset(n_rows=3000):
    data = []
    for _ in range(n_rows):
        data.append(generate_wheat_row())
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_wheat_dataset(3000)
    df.to_csv("wheat_fertilizer_dataset.csv", index=False)

    print("Dataset generated successfully")
    print(df.head())




    









