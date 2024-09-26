import pandas as pd

def my_round(raw):
    if pd.isna(raw):
        return raw
    else:
        return round(raw)