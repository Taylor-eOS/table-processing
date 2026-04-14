import sys
import pandas as pd

def load(path):
    if path.lower().endswith('.xlsx'):
        return pd.read_excel(path, dtype=str)
    return pd.read_csv(path, dtype=str)

def compare_csv(path_a, path_b):
    df_a = load(path_a)
    df_b = load(path_b)
    key_a = df_a.columns[0]
    key_b = df_b.columns[0]
    ids_a = set(df_a[key_a].dropna())
    ids_b = set(df_b[key_b].dropna())
    only_in_a = ids_a - ids_b
    only_in_b = ids_b - ids_a
    in_both = ids_a & ids_b
    total = len(ids_a | ids_b)
    print(f"File A: {path_a}")
    print(f"  Key column : '{key_a}'")
    print(f"  Total rows : {len(df_a)}")
    print(f"  Unique IDs : {len(ids_a)}")
    print()
    print(f"File B: {path_b}")
    print(f"  Key column : '{key_b}'")
    print(f"  Total rows : {len(df_b)}")
    print(f"  Unique IDs : {len(ids_b)}")
    print()
    print(f"Overlap")
    print(f"  Shared IDs        : {len(in_both):>6}  ({100 * len(in_both) / total:.1f}% of all unique IDs)")
    print(f"  Only in A         : {len(only_in_a):>6}  ({100 * len(only_in_a) / total:.1f}%)")
    print(f"  Only in B         : {len(only_in_b):>6}  ({100 * len(only_in_b) / total:.1f}%)")
    print()

    size_ratio = min(len(ids_a), len(ids_b)) / max(len(ids_a), len(ids_b)) if max(len(ids_a), len(ids_b)) else 1
    overlap_ratio = len(in_both) / total if total else 1

    if size_ratio < 0.5:
        smaller, bigger = ("A", "B") if len(ids_a) < len(ids_b) else ("B", "A")
        print(f"  WARNING: File {smaller} has less than half the unique IDs of file {bigger} ({size_ratio:.1%} size ratio).")
    if overlap_ratio < 0.5:
        print(f"  WARNING: Less than half of all IDs are shared between files ({overlap_ratio:.1%} overlap).")
    if size_ratio >= 0.5 and overlap_ratio >= 0.5:
        print(f"  OK: Files look broadly comparable.")

if __name__ == "__main__":
    compare_csv(input("First file: "), input("Second file: "))

