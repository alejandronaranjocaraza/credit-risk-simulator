from sklearn.preprocessing import StandardScaler


def standard_scale(df):
    numeric = list(df.select_dtypes(include=['number']).columns)
    scaler = StandardScaler()
    numeric_scaled = scaler.fit_transform(df[numeric])
    df_scaled = df.copy()
    df_scaled[numeric] = numeric_scaled
    return df_scaled
