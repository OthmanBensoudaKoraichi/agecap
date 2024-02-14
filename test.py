from utils import google_services

# Use the path to your service account key file
SERVICE_ACCOUNT_FILE = '/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/files/buoyant-apogee-411313-3fc58fa1faaa.json'

# Folder ID where the file should be uploaded
FOLDER_ID = '1jzqRv_SvUz1EkeV0AnlgY00PaTKhXjm4'  # Replace with your actual folder ID

# Specify the filename and path of the PDF file to upload
filename = 'sehassur_test'
filepath = "/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/files/Fiche produit SEHASSUR.pdf"

# Upload the file
google_services.upload_file_to_google_drive(SERVICE_ACCOUNT_FILE, filename, filepath, FOLDER_ID, mimetype='application/pdf')

data = [*family_details, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), query, response]
