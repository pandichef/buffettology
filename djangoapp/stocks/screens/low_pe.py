import pandas as pd
from .utils import get_current_sip_dataframe


def low_pe() -> pd.DataFrame:
    df = get_current_sip_dataframe()
    df = df[df.mlt_pe.astype(float) < 10.0]
    return df
