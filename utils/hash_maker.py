import hashlib

def make_hash(souscripteur_first_name,souscripteur_surname,souscripteur_dob):
    # Concatenate the inputs with a separator to ensure uniqueness
    concatenated_inputs = f"{souscripteur_first_name}|{souscripteur_surname}|{souscripteur_dob}"

    # Use hashlib to create a hash of the concatenated string
    # Here we use SHA-256, but you can choose different algorithms depending on your needs
    hash_object = hashlib.sha256(concatenated_inputs.encode())
    hex_dig = hash_object.hexdigest()

    # You may want to truncate the hash to a certain length for convenience
    return f'AM-{hex_dig[:6]}'  # Taking the first 10 characters for simplicity
