from sklearn.preprocessing import StandardScaler
import pandas as pd


def scale(df, cols):
    scaler = StandardScaler()
    res = df.copy()
    res[cols] = scaler.fit_transform(df[cols])
    return res


def one_hot_encode(df, cols, drop_first=True):
    res = df.copy()
    res = pd.get_dummies(
        df, columns=cols, drop_first=drop_first).astype(int)
    return res
