import pandas as pd
import statsmodels.api as sm
import numpy as np
import io
from contextlib import redirect_stdout
from typing import Tuple
from .utils import add_new_column_info


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
    details = "sloan_score"
    # return (df, details, new_columns)
    return (df, details)
