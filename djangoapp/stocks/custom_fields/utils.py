from typing import Callable, Tuple
import pandas as pd
from functools import wraps


def add_new_column_info(
    func: Callable[..., Tuple[pd.DataFrame, str]]
) -> Callable[..., Tuple[pd.DataFrame, str, Tuple[str, ...]]]:
    @wraps(func)
    def wrapper(
        df: pd.DataFrame, *args, **kwargs
    ) -> Tuple[pd.DataFrame, str, Tuple[str, ...]]:
        original_columns = set(df.columns.to_list())

        # Call the decorated function
        df, details = func(df, *args, **kwargs)

        # Determine new columns
        final_columns = set(df.columns.to_list())
        new_columns = tuple(final_columns - original_columns)

        return df, details, new_columns

    return wrapper
