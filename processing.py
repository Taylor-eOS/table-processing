import pandas as pd

def filter_csv(input_file, output_file, column, value):
    df = pd.read_csv(input_file, dtype=str)
    filtered_df = df[df[column] == value]
    filtered_df.to_csv(output_file, index=False)

filter_csv("cvr1.csv", "filtered.csv", "Hovedbranche", "433410 Maleraktiviteter")

