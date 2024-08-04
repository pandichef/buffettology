import os
from datetime import datetime
import pandas as pd
from django.conf import settings


def get_current_sip_dataframe() -> pd.DataFrame:
    sip_file_path = os.path.join(
        settings.MEDIA_ROOT, datetime.now().strftime("%Y%m%d") + ".parquet"
    )
    sip_df = pd.read_parquet(sip_file_path)
    return sip_df
