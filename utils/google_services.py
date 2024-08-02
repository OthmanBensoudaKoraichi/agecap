from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import ssl
import requests
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread

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

def get_last_filled_row(sheet,num_devis = None):
    if 'last_filled_row' not in st.session_state:
        st.session_state.last_filled_row = None
    if st.session_state.last_filled_row == None and num_devis == None:
        # Assume we're using column A to check for the last filled row
        column_a = sheet.col_values(1)  # Get all values from column A
        # I also note the first column corresponding to the chatbot's outputs
        column_n = sheet.col_values(16)

        # Note the last filled row number
        last_filled_row_a = len(column_a) + 1
        last_filled_row_n = len(column_n) + 1

        last_row = max(last_filled_row_a, last_filled_row_n)
        st.session_state.last_filled_row = last_row

    elif st.session_state.last_filled_row == None and num_devis != None:
        list_quote_numbers = sheet.col_values(7)
        row_index = list_quote_numbers.index(num_devis) + 1
        st.session_state.last_filled_row = row_index


    else:
        pass

    return st.session_state.last_filled_row

def append_data_to_sheet(type,sheet, data,num_devis = None,quote_calculated = False):
    """
    Appends a row of data to the specified Google Sheet.

    Args:
    sheet: The worksheet object obtained from gspread, representing the specific sheet to append data to.
    data: A list of data to append. Each element in the list corresponds to a cell in the row.
    """

    # Get last row filled
    last_filled_row = get_last_filled_row(sheet,num_devis)


    if type == "form":
        try:
            range_to_update = f'A{last_filled_row }:O{last_filled_row}'
            sheet.update(range_to_update, data)
            print("Data appended successfully.")
        except Exception as e:
            print(f"An error occurred while appending data to the sheet: {e}")

    if type == "chat":
        try:
            # Fetch the entire row (assuming you know the maximum number of columns, say 50)
            row_values = sheet.row_values(last_filled_row, value_render_option='FORMATTED_VALUE')

            # Find the last filled column in that row
            last_filled_column = len(row_values) - next((i for i, cell in enumerate(reversed(row_values)) if cell), -1)


            number_of_interactions = len(st.session_state.messages) // 2  # Using integer division for pairs
            if quote_calculated == False:

                ascii_value = ord(
                    'P') + number_of_interactions - 1
            else:
                ascii_value =  ord('P') + last_filled_column - 1

            column_letter = chr(ascii_value)

            cell_to_update = f'{column_letter}{last_filled_row}'
            sheet.update(cell_to_update, data)
            print("Data appended successfully.")
        except Exception as e:
            print(f"An error occurred while appending data to the sheet: {e}")

def append_questionnaire_status(sheet, status,num_devis):
    """
    Appends a row of data to the specified Google Sheet.

    Args:
    sheet: The worksheet object obtained from gspread, representing the specific sheet to append data to.
    data: A list of data to append. Each element in the list corresponds to a cell in the row.
    """
 # Get last row filled
    last_filled_row = get_last_filled_row(sheet,num_devis)

    try:
        cell_to_update = f'O{last_filled_row }'
        sheet.update(cell_to_update, status)
        print("Data appended successfully.")
    except Exception as e:
        print(f"An error occurred while appending data to the sheet: {e}")


# Example usage of the append_data_to_sheet function
#data_to_append = ["Example 2", "2024-02-12", "Example Query", "Example Response", "Example Chat History"]
#append_data_to_sheet(sheet, data_to_append)

ssl._create_default_https_context = ssl._create_unverified_context

def download_service_account_json(file_url):
    # Local path to save the downloaded file
    local_file_path = '/tmp/service_account.json'

    # Download the file
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        return local_file_path
    else:
        st.error("Une erreur est survenue. Veuillez nous excuser pour ce désagrément et nous contacter par téléphone au 05 22 22 41 80 ou sur l'adresse email assistance.agecap@gmail.com .")
        st.rerun()

def setup_google_drive(credentials_path, name_google_sheets):
    # Use credentials to setup Google Drive access
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path)
    file = gspread.authorize(creds)
    return file.open(name_google_sheets)