import pandas as pd

# Function to read a binary file and return its contents
def load_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

# Function to load excel data
def load_excel_data(primes_url, coefficients_url):
    primes = pd.read_excel(primes_url, sheet_name="primes")
    coefficients = pd.read_excel(coefficients_url, sheet_name="coefficients")
    return primes, coefficients