import pandas as pd
import statsmodels.api as sm
import numpy as np
import io
from contextlib import redirect_stdout
from typing import Tuple
from .utils import add_new_column_info


def backtest_sloan_score(df: pd.DataFrame) -> str:
    df = df.copy()
    df["return_12m"] = 100.0 * (
        df.psdc_price_m001.astype(float) / df.psdc_price_m012.astype(float) - 1.0
    )
    # original_columns = set(df.columns.to_list())
    df["backtest_rsst_accrual"] = (
        (
            df.bsa_ca_y1.astype(float)
            - df.bsa_ca_y2.astype(float)
            - df.bsa_cash_y1.astype(float)
            + df.bsa_cash_y2.astype(float)
            - df.bsa_cl_y1.astype(float)
            + df.bsa_cl_y2.astype(float)
            - df.bsa_stdebt_y1.astype(float)
            + df.bsa_stdebt_y2.astype(float)
        )
        + (
            df.bsa_assets_y1.astype(float)
            - df.bsa_assets_y2.astype(float)
            - df.bsa_ca_y1.astype(float)
            + df.bsa_ca_y2.astype(float)
            - df.bsa_oca_y1.astype(float)
            + df.bsa_oca_y2.astype(float)
            - df.bsa_liab_y1.astype(float)
            + df.bsa_liab_y2.astype(float)
            + df.bsa_cl_y1.astype(float)
            - df.bsa_cl_y2.astype(float)
            + df.bsa_ltdebt_y1.astype(float)
            - df.bsa_ltdebt_y2.astype(float)
        )
        + (
            df.bsa_stinv_y1.astype(float)
            - df.bsa_stinv_y2.astype(float)
            + df.bsa_oca_y1.astype(float)
            - df.bsa_oca_y2.astype(float)
            - df.bsa_ltdebt_y1.astype(float)
            + df.bsa_ltdebt_y2.astype(float)
            - df.bsa_stdebt_y1.astype(float)
            + df.bsa_stdebt_y2.astype(float)
            - df.bsa_pref_y1.astype(float)
            + df.bsa_pref_y2.astype(float)
        )
    ) / ((df.bsa_assets_y1.astype(float) + df.bsa_assets_y2.astype(float)) / 2)
    df["backtest_chg_receivables"] = (
        df.bsa_ar_y1.astype(float) - df.bsa_ar_y2.astype(float)
    ) / ((df.bsa_assets_y1.astype(float) + df.bsa_assets_y2.astype(float)) / 2)
    df["backtest_chg_inventory"] = np.where(
        (
            (df.bsa_inv_y1.astype(float) - df.bsa_inv_y2.astype(float))
            / ((df.bsa_assets_y1.astype(float) + df.bsa_assets_y2.astype(float)) / 2)
        )
        > -999,
        (
            (df.bsa_inv_y1.astype(float) - df.bsa_inv_y2.astype(float))
            / ((df.bsa_assets_y1.astype(float) + df.bsa_assets_y2.astype(float)) / 2)
        ),
        0,
    )
    df["backtest_soft_assets"] = (
        df.bsa_assets_y1.astype(float)
        - df.bsa_nppe_y1.astype(float)
        - df.bsa_cash_y1.astype(float)
    ) / df.bsa_assets_y1.astype(float)
    # Change Cash Sales
    df["backtest_chg_cash_sales"] = np.where(
        (
            (
                (df.isa_sales_y1.astype(float) - df.bsa_ar_y1.astype(float))
                - (df.isa_sales_y2.astype(float) - df.bsa_ar_y2.astype(float))
            )
            / (df.isa_sales_y2.astype(float) - df.bsa_ar_y2.astype(float))
        )
        > -99,
        (
            (
                (df.isa_sales_y1.astype(float) - df.bsa_ar_y1.astype(float))
                - (df.isa_sales_y2.astype(float) - df.bsa_ar_y2.astype(float))
            )
            / (df.isa_sales_y2.astype(float) - df.bsa_ar_y2.astype(float))
        ),
        0.08,
    )
    df["backtest_chg_earnings"] = df.isa_netinc_y1.astype(float) / (
        (df.bsa_assets_y1.astype(float) + df.bsa_assets_y2.astype(float)) / 2
    ) - df.isa_netinc_y2.astype(float) / (
        (df.bsa_assets_y2.astype(float) + df.bsa_assets_y3.astype(float)) / 2
    )
    df["backtest_issuance"] = np.where(
        (df.bsa_ltdebt_y1.astype(float) - df.bsa_ltdebt_y2.astype(float)) > 0,
        1,
        np.where((df.cfa_tcf_y1.astype(float) - df.cfa_tcf_y2.astype(float)) > 0, 1, 0),
    )

    df["backtest_sloan_score"] = (
        np.exp(
            -7.893
            + 0.79 * df.backtest_rsst_accrual.astype(float)
            + 2.518 * df.backtest_chg_receivables.astype(float)
            + 1.191 * df.backtest_chg_inventory.astype(float)
            + 1.979 * df.backtest_soft_assets.astype(float)
            + 0.171 * df.backtest_chg_cash_sales.astype(float)
            - 0.932 * df.backtest_chg_earnings.astype(float)
            + 1.029 * df.backtest_issuance.astype(float)
        )
        / (
            1
            + np.exp(
                -7.893
                + 0.79 * df.backtest_rsst_accrual.astype(float)
                + 2.518 * df.backtest_chg_receivables.astype(float)
                + 1.191 * df.backtest_chg_inventory.astype(float)
                + 1.979 * df.backtest_soft_assets.astype(float)
                + 0.171 * df.backtest_chg_cash_sales.astype(float)
                - 0.932 * df.backtest_chg_earnings.astype(float)
                + 1.029 * df.backtest_issuance.astype(float)
            )
        )
        / 0.0037
    )

    # final_columns = set(df.columns.to_list())
    # new_columns = tuple(final_columns - original_columns)
    # details = "sloan_score"
    # return (df, details, new_columns)
    # Create deciles for 'column1'
    df["decile"] = pd.qcut(
        df["backtest_sloan_score"], 10, labels=False
    )  # 10 for deciles

    # Compute the average value of 'column2' for each decile
    mean_sloan_score = df.groupby("decile")["backtest_sloan_score"].mean()
    mean_return_12m = df.groupby("decile")["return_12m"].mean()
    number_of_stocks = df.groupby("decile").size()

    # Redirect stdout to capture print output
    # with io.StringIO() as buf, redirect_stdout(buf):
    #     print(average_column2)
    #     output = buf.getvalue()
    results_df = pd.DataFrame(
        {
            "Sloan Score (mean)": mean_sloan_score,
            "12m Return (mean)": mean_return_12m,
            "Number of Stocks": number_of_stocks,
        }
    )

    return results_df.to_html()


@add_new_column_info
def gen_sloan_score(df: pd.DataFrame) -> Tuple[pd.DataFrame, str]:
    # original_columns = set(df.columns.to_list())
    df["_rsst_accrual"] = (
        (
            df.bsa_ca_y1.astype(float)
            - df.bsa_ca_y2.astype(float)
            - df.bsa_cash_y1.astype(float)
            + df.bsa_cash_y2.astype(float)
            - df.bsa_cl_y1.astype(float)
            + df.bsa_cl_y2.astype(float)
            - df.bsa_stdebt_y1.astype(float)
            + df.bsa_stdebt_y2.astype(float)
        )
        + (
            df.bsa_assets_y1.astype(float)
            - df.bsa_assets_y2.astype(float)
            - df.bsa_ca_y1.astype(float)
            + df.bsa_ca_y2.astype(float)
            - df.bsa_oca_y1.astype(float)
            + df.bsa_oca_y2.astype(float)
            - df.bsa_liab_y1.astype(float)
            + df.bsa_liab_y2.astype(float)
            + df.bsa_cl_y1.astype(float)
            - df.bsa_cl_y2.astype(float)
            + df.bsa_ltdebt_y1.astype(float)
            - df.bsa_ltdebt_y2.astype(float)
        )
        + (
            df.bsa_stinv_y1.astype(float)
            - df.bsa_stinv_y2.astype(float)
            + df.bsa_oca_y1.astype(float)
            - df.bsa_oca_y2.astype(float)
            - df.bsa_ltdebt_y1.astype(float)
            + df.bsa_ltdebt_y2.astype(float)
            - df.bsa_stdebt_y1.astype(float)
            + df.bsa_stdebt_y2.astype(float)
            - df.bsa_pref_y1.astype(float)
            + df.bsa_pref_y2.astype(float)
        )
    ) / ((df.bsa_assets_y1.astype(float) + df.bsa_assets_y2.astype(float)) / 2)
    df["_chg_receivables"] = (
        df.bsa_ar_y1.astype(float) - df.bsa_ar_y2.astype(float)
    ) / ((df.bsa_assets_y1.astype(float) + df.bsa_assets_y2.astype(float)) / 2)
    df["_chg_inventory"] = np.where(
        (
            (df.bsa_inv_y1.astype(float) - df.bsa_inv_y2.astype(float))
            / ((df.bsa_assets_y1.astype(float) + df.bsa_assets_y2.astype(float)) / 2)
        )
        > -999,
        (
            (df.bsa_inv_y1.astype(float) - df.bsa_inv_y2.astype(float))
            / ((df.bsa_assets_y1.astype(float) + df.bsa_assets_y2.astype(float)) / 2)
        ),
        0,
    )
    df["_soft_assets"] = (
        df.bsa_assets_y1.astype(float)
        - df.bsa_nppe_y1.astype(float)
        - df.bsa_cash_y1.astype(float)
    ) / df.bsa_assets_y1.astype(float)
    # Change Cash Sales
    df["_chg_cash_sales"] = np.where(
        (
            (
                (df.isa_sales_y1.astype(float) - df.bsa_ar_y1.astype(float))
                - (df.isa_sales_y2.astype(float) - df.bsa_ar_y2.astype(float))
            )
            / (df.isa_sales_y2.astype(float) - df.bsa_ar_y2.astype(float))
        )
        > -99,
        (
            (
                (df.isa_sales_y1.astype(float) - df.bsa_ar_y1.astype(float))
                - (df.isa_sales_y2.astype(float) - df.bsa_ar_y2.astype(float))
            )
            / (df.isa_sales_y2.astype(float) - df.bsa_ar_y2.astype(float))
        ),
        0.08,
    )
    df["_chg_earnings"] = df.isa_netinc_y1.astype(float) / (
        (df.bsa_assets_y1.astype(float) + df.bsa_assets_y2.astype(float)) / 2
    ) - df.isa_netinc_y2.astype(float) / (
        (df.bsa_assets_y2.astype(float) + df.bsa_assets_y3.astype(float)) / 2
    )
    df["_issuance"] = np.where(
        (df.bsa_ltdebt_y1.astype(float) - df.bsa_ltdebt_y2.astype(float)) > 0,
        1,
        np.where((df.cfa_tcf_y1.astype(float) - df.cfa_tcf_y2.astype(float)) > 0, 1, 0),
    )

    df["_sloan_score"] = (
        np.exp(
            -7.893
            + 0.79 * df._rsst_accrual.astype(float)
            + 2.518 * df._chg_receivables.astype(float)
            + 1.191 * df._chg_inventory.astype(float)
            + 1.979 * df._soft_assets.astype(float)
            + 0.171 * df._chg_cash_sales.astype(float)
            - 0.932 * df._chg_earnings.astype(float)
            + 1.029 * df._issuance.astype(float)
        )
        / (
            1
            + np.exp(
                -7.893
                + 0.79 * df._rsst_accrual.astype(float)
                + 2.518 * df._chg_receivables.astype(float)
                + 1.191 * df._chg_inventory.astype(float)
                + 1.979 * df._soft_assets.astype(float)
                + 0.171 * df._chg_cash_sales.astype(float)
                - 0.932 * df._chg_earnings.astype(float)
                + 1.029 * df._issuance.astype(float)
            )
        )
        / 0.0037
    )

    # final_columns = set(df.columns.to_list())
    # new_columns = tuple(final_columns - original_columns)
    details = backtest_sloan_score(df)
    # return (df, details, new_columns)
    return (df, details)
