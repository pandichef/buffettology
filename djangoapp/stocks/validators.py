import os
import pandas as pd
from django.core.exceptions import ValidationError


def validate_parquet_file(value):
    try:
        # Read the file content and attempt to load it with pandas
        value.seek(0)  # Ensure we start reading from the beginning of the file
        pd.read_parquet(value)  # Will fail if not a valid Parquet file
    except (ValueError, OSError) as e:
        raise ValidationError("This file is not a valid Parquet file.") from e

    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in [".parquet"]:
        raise ValidationError(
            f"Unsupported file extension. Only Parquet files are allowed."
        )
