import requests

# The raw URL of the Excel file on GitHub
excel_url = 'https://raw.githubusercontent.com/OthmanBensoudaKoraichi/agecap/master/files/sehassur_devis.xlsx'

# The local path where you want to save the downloaded Excel file
save_path = 'sehassur_devis.xlsx'

# Attempt to download the Excel file
response = requests.get(excel_url)

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    # Write the content of the response (the Excel file) to a local file
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f"Excel file was successfully downloaded and saved as '{save_path}'.")
else:
    print(f"Failed to download the Excel file. HTTP status code: {response.status_code}")
