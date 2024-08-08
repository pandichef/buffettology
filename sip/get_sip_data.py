# import os
# import geopandas as gpd


# def convert_dbf_to_csv(input_folder, output_folder):
#     files_with_company_id = []

#     # Iterate through all files and directories recursively
#     for root, dirs, files in os.walk(input_folder):
#         for file in files:
#             if file.lower().endswith(".dbf"):
#                 dbf_path = os.path.join(root, file)
#                 print(f"Converting {dbf_path} to CSV...")

#                 # Read the .dbf file using geopandas
#                 try:
#                     gdf = gpd.read_file(dbf_path)
#                 except Exception as e:
#                     print(f"Error reading {dbf_path}: {e}")
#                     continue

#                 # Check if 'COMPANY_ID' column exists
#                 if "COMPANY_ID" in gdf.columns:
#                     files_with_company_id.append(file)

#                 # Prepare output CSV filename
#                 csv_filename = os.path.splitext(file)[0] + ".csv"
#                 output_path = os.path.join(output_folder, csv_filename)

#                 # Save as CSV
#                 try:
#                     gdf.to_csv(output_path, index=False)
#                     print(f"Saved {csv_filename} to {output_folder}")
#                 except Exception as e:
#                     print(f"Error saving {csv_filename} to {output_folder}: {e}")

#     # Print list of files with COMPANY_ID column
#     if files_with_company_id:
#         print(
#             f"\nFiles with 'COMPANY_ID' column (total: {len(files_with_company_id)}):"
#         )
#         for file in files_with_company_id:
#             print(file)


import os
import geopandas as gpd
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from typing import Tuple
from custom_fields.gen_logit_pd import gen_logit_pd
from custom_fields.gen_sloan_score import gen_sloan_score


# pd.DataFrame.to_parquet
# def to_parquet_with_metadata(df: pd.DataFrame, path: str, metadata: dict) -> None:
def to_parquet_with_metadata(df: pd.DataFrame, path: str) -> None:
    # if df.index.name:

    #     df['__index_level_0__'] =

    custom_metadata = df.metadata
    # Sample DataFrame
    # df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

    # Convert DataFrame to PyArrow Table
    table = pa.Table.from_pandas(df)

    import json
    from copy import copy

    new_metadata = copy(table.schema.metadata)
    encoded_custom_metadata = json.dumps(custom_metadata).encode("utf-8")
    new_metadata.update({b"custom": encoded_custom_metadata})

    # table.schema.metadata.update({b"custom_metadata": encoded_custom_metadata})

    # Define metadata
    # metadata = {"source": "data_source.csv", "created_by": "David"}
    # new_metadata_bytes = {k: str(v).encode("utf-8") for k, v in metadata.items()}

    # Add metadata to the table's schema
    table = table.replace_schema_metadata(new_metadata)

    # Save to Parquet
    pq.write_table(table, path)


# def read_parquet_with_metadata(
#     path: str, index_name: str | None = None
# ) -> Tuple[pd.DataFrame, dict]:
#     read_table = pq.read_table(path)
#     df = read_table.to_pandas()
#     metadata_bytes = read_table.schema.metadata
#     metadata = {
#         key.decode("utf-8"): value.decode("utf-8")
#         for key, value in metadata_bytes.items()
#     }

#     if index_name:
#         df = df.set_index(index_name)

#     return df, metadata


# from probability_model import add_default_probability

# Define the base directory path
base_dir = os.getenv("SIP_DIR_PATH")

# List of files to process
file_paths = [
    "Dbfs/si_perc.dbf",
    "Static/si_bsa.dbf",
    "Static/si_bsq.dbf",
    "Static/si_cfa.dbf",
    "Static/si_cfq.dbf",
    "Static/si_ci.dbf",
    "Static/si_date.dbf",
    "Dbfs/si_ee.dbf",
    "Dbfs/si_gr.dbf",
    "Static/si_isa.dbf",
    "Static/si_isq.dbf",
    "Dbfs/si_mlt.dbf",
    "Dbfs/si_psd.dbf",
    "Dbfs/si_psda.dbf",
    "Dbfs/si_psdd.dbf",
    "Dbfs/si_psdc.dbf",
    "Dbfs/si_psdh.dbf",
    "Dbfs/si_psdl.dbf",
    "Dbfs/si_psdv.dbf",
    "Dbfs/si_rat.dbf",
    "Dbfs/si_val.dbf",
]

# Initialize an empty list to store GeoDataFrames
gdfs = []

# Read each .dbf file into a GeoDataFrame
for file_path in file_paths:
    file_full_path = os.path.join(base_dir, file_path)  # type: ignore
    try:
        gdf = gpd.read_file(file_full_path)
        if "_NullFlags" in gdf.columns:
            gdf.drop("_NullFlags", axis=1, inplace=True)
        if "LASTMOD" in gdf.columns:
            gdf.drop("LASTMOD", axis=1, inplace=True)
        if "UPDATED" in gdf.columns:
            gdf.drop("UPDATED", axis=1, inplace=True)
        if "REPNO" in gdf.columns:
            gdf.drop("REPNO", axis=1, inplace=True)

        source_identifier = file_path.split("/")[1].split(".")[0][3:]  # remove "si_"
        gdf.columns = [
            f"{source_identifier}_{col.lower()}"
            if col.lower() != "company_id"
            else col.lower()
            for col in gdf.columns
        ]

        gdfs.append(gdf)
        print(f"Read {file_path} successfully.")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Merge all GeoDataFrames on 'COMPANY_ID'
if gdfs:
    merged_df = gdfs[0]
    for df in gdfs[1:]:
        merged_df = pd.merge(merged_df, df, on="company_id", how="outer")

    # Print summary
    print(f"Merged DataFrame shape: {merged_df.shape}")
    print(merged_df.head())

    # Optionally, save merged DataFrame to a CSV file
    # merged_csv_path = os.path.join(base_dir, "merged_data.csv")
    # merged_df.to_csv("merged_data.csv", index=False)
    merged_df.set_index("ci_ticker", inplace=True)

    # df_add_probability, result = add_default_probability(merged_df)
    # df_add_probability.result = result
    df = merged_df
    # df2.metadata = {"source": "data_source.csv", "created_by": "David"}

    # df2, details, new_columns = gen_sloan_score(df2)
    # df2, details, new_columns = gen_logit_pd(df2)

    custom_field_script_list = [gen_sloan_score, gen_logit_pd]
    custom_field_script_results = []
    for custom_field_script in custom_field_script_list:
        df, details, new_columns = custom_field_script(df)
        custom_field_script_results.append(
            (custom_field_script.__name__, details, new_columns)
        )
    print(custom_field_script_results)
    # assert False
    df.metadata = {"custom_field_scripts": custom_field_script_results}

    if False:
        df.to_parquet("merged_data.parquet")
    else:
        to_parquet_with_metadata(
            df,
            "merged_data.parquet",
            # {"source": "data_source.csv", "created_by": "David"},
        )
    # merged_df.to_parquet("merged_data.parquet", index=False)
    print(f"Saved merged data to parquet file")
else:
    print("No GeoDataFrames were successfully read. Check your file paths and data.")
