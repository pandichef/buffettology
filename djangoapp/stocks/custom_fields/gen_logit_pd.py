import pandas as pd
import statsmodels.api as sm
import numpy as np
import io
from contextlib import redirect_stdout
from typing import Tuple
from .utils import add_new_column_info


@add_new_column_info
def gen_logit_pd(df: pd.DataFrame,) -> Tuple[pd.DataFrame, str]:
    # original_columns = set(df.columns.to_list())
    # original_column_count = df.shape[1]
    df["return_12m"] = 100.0 * (
        df.psdc_price_m001.astype(float) / df.psdc_price_m012.astype(float) - 1.0
    )

    df["default_proxy"] = np.where(df["return_12m"] < -50, 1, 0)
    # Assuming you have a DataFrame 'df' with the necessary covariates and the target variable
    # df = pd.read_csv('your_data.csv')  # Replace with your data loading method

    # Define the covariates
    covariates2 = [  # used in regression
        "rat_quick_y2",
        "rat_curr_y2",
        "rat_ltd_eq_y2",
        "rat_tie_y2",
        "rat_zscore_y2",
    ]
    covariates1 = [  # to generate predicted PD
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

    #########################
    # FIT MODEL USING Y2 DATA
    # Add a constant term to the covariates
    X2 = sm.add_constant(df_clean[covariates2])

    # Define the target variable
    # y = df["return_12m"]
    y = df_clean["default_proxy"]

    # Fit the logistic regression model
    logit_model = sm.Logit(y, X2)
    result = logit_model.fit()

    #########################
    # GENERATE PD USING Y1 DATA
    X1 = sm.add_constant(df[covariates1])
    df["qt_pd"] = result.predict(X1) * 100

    # Print the summary of the logistic regression model
    with io.StringIO() as buf, redirect_stdout(buf):
        print(result.summary())
        qt_pd_regression_summary = buf.getvalue()

    # final_column_count = df.shape[1]
    # final_columns = df.columns.to_list()
    del df["return_12m"]
    del df["default_proxy"]
    details = qt_pd_regression_summary

    # final_columns = set(df.columns.to_list())
    # new_columns = tuple(final_columns - original_columns)
    # assert final_column_count == original_column_count + 1

    return (
        df,
        details,
        # new_columns,
    )
