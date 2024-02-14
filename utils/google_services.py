from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# The scopes required by the app. If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def authenticate_google_drive(service_account_file):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    return service

def upload_file_to_google_drive(service_account_file, filename, filepath, folder_id=None, mimetype='application/pdf'):
    service = authenticate_google_drive(service_account_file)
    file_metadata = {'name': filename}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File ID: {file.get('id')}")


def append_data_to_sheet(sheet, data):
    """
    Appends a row of data to the specified Google Sheet.

    Args:
    sheet: The worksheet object obtained from gspread, representing the specific sheet to append data to.
    data: A list of data to append. Each element in the list corresponds to a cell in the row.
    """
    try:
        # Append the data to the last row of the sheet
        sheet.append_row(data, value_input_option='USER_ENTERED')
        print("Data appended successfully.")
    except Exception as e:
        print(f"An error occurred while appending data to the sheet: {e}")

# Example usage of the append_data_to_sheet function
#data_to_append = ["Example 2", "2024-02-12", "Example Query", "Example Response", "Example Chat History"]
#append_data_to_sheet(sheet, data_to_append)