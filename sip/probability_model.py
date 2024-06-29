import pandas as pd
import statsmodels.api as sm
import numpy as np


def add_default_probability(df):
    # df = pd.read_parquet("/django_media_dev/20240628.parquet")

    df["return_12m"] = 100.0 * (
        df.psdc_price_m001.astype(float) / df.psdc_price_m012.astype(float) - 1.0
    )

    df["default_proxy"] = np.where(df["return_12m"] < -50, 1, 0)
    # Assuming you have a DataFrame 'df' with the necessary covariates and the target variable
    # df = pd.read_csv('your_data.csv')  # Replace with your data loading method

    # Define the covariates
    covariates2 = [
        "rat_quick_y2",
        "rat_curr_y2",
        "rat_ltd_eq_y2",
        "rat_tie_y2",
        "rat_zscore_y2",
    ]
    covariates1 = [
        "rat_quick_y1",
        "rat_curr_y1",
        "rat_ltd_eq_y1",
        "rat_tie_y1",
        "rat_zscore_y1",
    ]

    df_clean = df.dropna(subset=covariates2 + ["default_proxy"])

    for covariate in covariates2:
        df_clean[covariate] = df_clean[covariate].astype(float)
        df[covariate] = df[covariate].astype(float)
    for covariate in covariates1:
        df_clean[covariate] = df_clean[covariate].astype(float)
        df[covariate] = df[covariate].astype(float)

    # Add a constant term to the covariates
    X2 = sm.add_constant(df_clean[covariates2])

    # Define the target variable
    # y = df["return_12m"]
    y = df_clean["default_proxy"]

    # Fit the logistic regression model
    logit_model = sm.Logit(y, X2)
    result = logit_model.fit()

    # Print the summary of the logistic regression model
    print(result.summary())

    # fit data
    X1 = sm.add_constant(df[covariates1])
    df["default_prediction"] = result.predict(X1) * 100
    df[["default_prediction", "rat_zscore_y1", "rat_zscore_y2"]].to_clipboard()

    return df, result
