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
import json


def read_parquet_with_metadata(path) -> pd.DataFrame:
    table = pq.read_table(path)
    # index_name = json.loads(table.schema.metadata[b"pandas"].decode("utf-8"))[
    #     "index_columns"
    # ][0]
    df = table.to_pandas()
    custom_metadata = json.loads(table.schema.metadata[b"custom"].decode("utf-8"))
    # metadata = {
    #     key.decode("utf-8"): value.decode("utf-8")
    #     for key, value in metadata_bytes.items()
    # }

    # if index_name:
    #     df = df.set_index(index_name)

    df.metadata = custom_metadata

    return df


def get_current_sip_dataframe() -> pd.DataFrame:
    sip_file_path = os.path.join(
        settings.MEDIA_ROOT, datetime.now().strftime("%Y%m%d") + ".parquet"
    )
    # sip_df = pd.read_parquet(sip_file_path)
    sip_df = read_parquet_with_metadata(sip_file_path)
    # print("metadata")
    # print(sip_df.metadata)
    return sip_df
