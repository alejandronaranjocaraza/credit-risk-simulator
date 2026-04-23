import pandas as pd


def one_hot_encode(df):
    non_numeric = list(df.select_dtypes(exclude=['number']).columns)
    df_encoded = pd.get_dummies(
        df, columns=non_numeric, drop_first=True).astype(int)
    return df_encoded
