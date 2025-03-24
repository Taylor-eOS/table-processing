import pandas as pd

def filter_csv(input_file, output_file, postnr_list):
    df = pd.read_csv(input_file, dtype=str)
    df = df[df["Postnr."].isin(postnr_list)]
    df.to_csv(output_file, index=False)

filter_csv("input.csv", "filtered.csv", ["1000"])

