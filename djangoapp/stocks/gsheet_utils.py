import io
import os
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

sip_field_type = {
    "perc": "% Rank",
    "bsa": "Balance Sheet - Annual",
    "bsq": "Balance Sheet - Quarterly",
    "cfa": "Cash Flow - Annual",
    "cfq": "Cash Flow - Quarterly",
    "ci": "Company Information",
    "date": "Dates and Periods",
    "ee": "Earnings Estimates",
    "gr": "Growth Rates",
    "isa": "Income Statement - Annual",
    "isq": "Income Statement - Quarterly",
    "mlt": "Multiples",
    "psd": "Price and Share Statistics",
    "psda": "Prices - Annual",
    "psdd": "Prices - Dates",
    "psdc": "Prices - Monthly Close",
    "psdh": "Prices - Monthly High",
    "psdl": "Prices - Monthly Low",
    "psdv": "Prices - Monthly Volume",
    "rat": "Ratios",
    "val": "Valuations",
}

try:
    # Authenticate with Google Drive API
    creds = service_account.Credentials.from_service_account_file(
        "client_secrets.json", scopes=["https://www.googleapis.com/auth/drive"]
    )
    file_location = "client_secrets.json"
except:
    # Authenticate with Google Drive API
    creds = service_account.Credentials.from_service_account_file(
        "../client_secrets.json", scopes=["https://www.googleapis.com/auth/drive"]
    )
    file_location = "../client_secrets.json"

drive_service = build("drive", "v3", credentials=creds)


def create_google_sheet(filename: str, df: pd.DataFrame) -> str:
    # NOT USED: I decided to use Excel instead to be able to work locally
    # NOT USED: I decided to use Excel instead to be able to work locally
    # NOT USED: I decided to use Excel instead to be able to work locally
    import pygsheets

    gc = pygsheets.authorize(service_file=file_location)
    # Create a new Google Sheet
    spreadsheet = gc.create(filename)
    spreadsheet_id = spreadsheet.id
    print(f"Created Google Sheet with ID: {spreadsheet_id}")

    # Specify the folder ID where you want to place the Google Sheet

    folder_id = os.environ["BUFFETTOLOGY_FOLDER_ID"]  # Replace with your folder ID

    # Function to move the Google Sheet to a specific folder
    def move_file_to_folder(drive_service, file_id, folder_id):
        # Move to folder with public access
        # Retrieve the file's current metadata
        file = drive_service.files().get(fileId=file_id, fields="parents").execute()
        current_parents = file.get("parents")

        print("current_parents")
        print(current_parents)

        # Move the file to the new folder
        if current_parents:
            # Remove file from current parents
            for parent in current_parents:
                drive_service.files().update(
                    fileId=file_id, removeParents=parent, fields="id, parents"
                ).execute()

        # Add the file to the new folder
        drive_service.files().update(
            fileId=file_id, addParents=folder_id, fields="id, parents"
        ).execute()

    # Move the Google Sheet to the specified folder
    move_file_to_folder(drive_service, spreadsheet_id, folder_id)

    print(f"Moved the Google Sheet to folder with ID: {folder_id}")
    print(f"Permissions updated. Anyone with the link can now view the sheet.")

    # Update the content of the Google Sheet
    # worksheet = spreadsheet.sheet1
    # worksheet.update_value("A1", "Hello, World!")
    # Create a sample DataFrame

    # Create multiple tab for each data field type
    for field_type in sip_field_type:
        filtered_df = df[df["name"].str.startswith(field_type + "_")]
        worksheet = spreadsheet.add_worksheet(
            title=sip_field_type[field_type]
        )  # You can specify the number of rows and columns
        worksheet.set_dataframe(
            df=filtered_df, start=(1, 1), copy_index=False, copy_head=True
        )

    # delete sheet1
    # pygsheets creates this by default
    worksheet = spreadsheet.sheet1
    spreadsheet.del_worksheet(worksheet)

    # Print the link to the Google Sheet
    sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
    print(f"Link to the Google Sheet: {sheet_url}")
    return sheet_url


def create_excel_sheet(filename: str, df: pd.DataFrame) -> str:
    # # Create an Excel file in memory
    # excel_buffer = io.BytesIO()
    # with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
    #     df.to_excel(writer, index=False)
    # excel_buffer.seek(0)  # Move the buffer position to the beginning

    # Create an Excel file in memory
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        for field_type in sip_field_type:
            filtered_df = df[df["name"].str.startswith(field_type + "_")]
            sheet_name = sip_field_type[field_type]
            filtered_df.to_excel(writer, sheet_name=sheet_name, index=False)
    excel_buffer.seek(0)  # Move the buffer position to the beginning

    print(f"Created Excel file in memory.")

    # Upload the Excel file to Google Drive
    folder_id = os.environ["BUFFETTOLOGY_FOLDER_ID"]  # Replace with your folder ID
    file_metadata = {
        "name": f"{filename}.xlsx",
        "parents": [folder_id],
    }  # Specify the parent folder ID
    media = MediaIoBaseUpload(
        excel_buffer,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    file = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    file_id = file.get("id")
    print(f"Uploaded Excel file to Google Drive with ID: {file_id}")

    # Print the link to the Google Drive file
    file_url = f"https://docs.google.com/spreadsheets/d/{file_id}"
    print(f"Link to the Excel file: {file_url}")
    return file_url


if __name__ == "__main__":
    df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [24, 30]})
    # create_google_sheet("META", df)
    create_excel_sheet("META", df)
