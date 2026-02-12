import pandas as pd

def load_and_standardize(file_path, crop_type):
    df = pd.read_csv(file_path)

    # unify day column
    if crop_type == "wheat":
        df.rename(columns={"days_since_sowing": "days_since_start"}, inplace=True)
    elif crop_type == "rice":
        df.rename(columns={"days_since_transplanting": "days_since_start"}, inplace=True)

    return df


def concat_datasets(wheat_file, rice_file):
    wheat_df = load_and_standardize(wheat_file, "wheat")
    rice_df = load_and_standardize(rice_file, "rice")

    final_df = pd.concat([wheat_df, rice_df], ignore_index=True)
    return final_df


rice_wheat_dataset = concat_datasets(
    "wheat_fertilizer_dataset.csv",
    "rice_fertilizer_dataset.csv"
)

print(rice_wheat_dataset.info())

rice_wheat_dataset.to_csv("final_dataset.csv", index=False)
