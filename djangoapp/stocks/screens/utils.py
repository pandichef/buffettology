import os
from datetime import datetime
import pandas as pd
from django.conf import settings
import os

# import geopandas as gpd
import pandas as pd

# import pyarrow as pa
import pyarrow.parquet as pq
from typing import Tuple


def read_parquet_with_metadata(
    path, index_name: str | None = None
) -> Tuple[pd.DataFrame, dict]:
    read_table = pq.read_table(path)
    df = read_table.to_pandas()
    metadata_bytes = read_table.schema.metadata
    metadata = {
        key.decode("utf-8"): value.decode("utf-8")
        for key, value in metadata_bytes.items()
    }

    if index_name:
        df = df.set_index(index_name)

    return df, metadata


def get_current_sip_dataframe() -> pd.DataFrame:
    sip_file_path = os.path.join(
        settings.MEDIA_ROOT, datetime.now().strftime("%Y%m%d") + ".parquet"
    )
    # sip_df = pd.read_parquet(sip_file_path)
    sip_df, metadata = read_parquet_with_metadata(sip_file_path, index_name="ci_ticker")
    print("metadata")
    print(metadata)
    return sip_df
