import pandas as pd

def filter_in_branches(input_file, output_file, include_contains):
    df = pd.read_csv(input_file, dtype=str)

    if include_contains:
        df = df[df["Hovedbranche"].str.contains("|".join(include_contains), na=False, case=False, regex=True)]

    df.to_csv(output_file, index=False)

filter_in_branches(
    "filtered.csv", 
    "filtered_list.csv",
    include_contains=["Example industry", "Other industry"])

