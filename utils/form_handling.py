import datetime
import pandas as pd
import streamlit as st
from utils import calculation, function_check, doc_manip,google_services, config,data_loaders, hash_maker, email_sender
from streamlit_extras.switch_page_button import switch_page
import tempfile
import requests

def process_form_submission(credentials,workbook):

    primes, coefficients = data_loaders.load_excel_data(config.primes_and_coef, config.primes_and_coef)
    # Initialize session state for family members count
    if "family_count" not in st.session_state:
        st.session_state["family_count"] = 1

    if 'quote_calculated' not in st.session_state:
        st.session_state.quote_calculated = False


    with st.form("insurance_form"):
        member_over_60_found = False
        family_details = []
        all_fields_filled = True  # Assume all fields are initially filled
        phone_valid = True
        email_valid = True
        temp_file_path = None
        nb_adultes = 0
        nb_enfants = 0

        # Input fields for family members
        if "family_count" not in st.session_state:
            st.session_state["family_count"] = 3  # Supposons 3 pour l'exemple

        for i in range(st.session_state["family_count"]):
            expanded = True  # Expand all by default

            # Adjusting member labels based on index
            if i == 0:
                member_label = "Souscripteur (Vous)"
                relation_type = 'Souscripteur'
            else:
                member_label = f"Membre de la famille {i}"

            with st.expander(member_label, expanded=expanded):
                # For family members beyond the first, add a selectbox to choose between Conjoint(e) and Enfant
                if i > 0:
                    relation_type = st.selectbox(
                        "Relation au souscripteur",
                        options=["Conjoint(e)", "Enfant"],
                        index=0 if i == 1 else 1,  # Default to Conjoint(e) for the first and Enfant thereafter
                        key=f"relation_{i}"
                    )

                # Condition pour afficher les champs Prénom et Nom de famille uniquement pour le souscripteur
                if i == 0:
                    first_name = st.text_input("Prénom *", key=f"first_name_{i}")
                    surname = st.text_input("Nom de famille *", key=f"surname_{i}")

                day_options = list(range(1, 32))  # Possible day values
                month_options = config.months
                current_year = datetime.datetime.now().year
                year_options = list(range(current_year - 100, current_year + 1))  # Last 100 years

                # Using st.columns to align day, month, and year on the same line
                col1, col2, col3 = st.columns(3)
                with col1:
                    selected_day = st.selectbox("Jour de naissance", options=day_options, index=0, key=f"day_{i}")
                with col2:
                    selected_month = st.selectbox("Mois de naissance", options=month_options.keys(), index=0, key=f"month_{i}")
                with col3:
                    selected_year = st.selectbox("Année de naissance", options=year_options, index=25,
                                                 key=f"year_{i}")  # Default to 25 years ago

                # Constructing the datetime object for the date of birth
                dob = datetime.datetime(year=selected_year, month=month_options[selected_month], day=selected_day)

                # Append the details to the family_details list
                if i == 0:
                    family_details.append((first_name, surname, dob, relation_type))
                else:
                    # For additional family members where first_name and surname may not be defined
                    family_details.append(("", "", dob, relation_type))
                # Calculate age from dob and set flag if over 60
                age = calculation.calculate_age(dob)
                if age < 20:
                    nb_enfants += 1
                if age >= 20:
                    nb_adultes += 1
                if age > 60:
                    member_over_60_found = True

            # Display warning if the maximum number of family members is reached
            if i == 6:  # Check if this is the 7th family member (index 6)
                st.warning("Le maximum de 7 membres a été atteint.")


        # Button to add family members within the form
        st.form_submit_button(
            "Ajouter un membre de la famille",
            on_click=function_check.increment_family_count,
        )


        # Validate souscripteur details
        souscripteur_first_name = st.session_state.get("first_name_0", "")
        souscripteur_surname = st.session_state.get("surname_0", "")
        if not souscripteur_first_name or not souscripteur_surname:
            all_fields_filled = False

        if "email_address" not in st.session_state:
            st.session_state["email_address"] = None
        email_address = st.text_input("Adresse email du souscripteur *", key="email")
        st.session_state["email_address"] = email_address


        if email_address and not function_check.is_valid_email(email_address):
            email_valid = False
        elif not email_address:
            all_fields_filled = False


        phone_number = st.text_input("Numéro de téléphone du souscripteur *", key="phone").replace(
            " ", ""
        )
        if phone_number and not function_check.is_valid_number(phone_number):
            phone_valid = False
        elif not phone_number and not function_check.is_valid_number(phone_number):
            all_fields_filled = False

        # Select the medium, with index = 1 so that no medium is selected by default
        medium = st.radio(
            "Sur quel réseau social avez-vous vu notre formulaire? *",
            ('LinkedIn', 'Facebook', 'Instagram','Ne souhaite pas préciser'), index = 3
        )

        submit_button = st.form_submit_button("Calculer le devis")
        st.caption("Cela vous redirigera vers votre devis en quelques secondes.")

        if submit_button:
            if 'id_devis' not in st.session_state:
                st.session_state.id_devis = ''
            # Create id_devis
            id_devis = hash_maker.make_hash(family_details[0][0],family_details[0][1],family_details[0][1])
            st.session_state.id_devis = id_devis

            if phone_valid == False:
                st.error("Format du numéro de téléphone invalide")
            if email_valid == False:
                st.error("Format de l'adresse email invalide")
            # Check if a medium has been selected
            if medium not in ('LinkedIn', 'Facebook', 'Instagram','Ne souhaite pas préciser'):
                st.error("La sélection d'un réseau social est obligatoire.")
                all_fields_filled = False
            # Final submit button is only enabled if all family members are below 60
            if member_over_60_found and all_fields_filled:
                data_append_old = [
                    [family_details[0][0], family_details[0][1], family_details[0][2].strftime("%d-%m-%Y"), email_address, phone_number,
                     medium, "Pas de devis", datetime.datetime.today().strftime("%d-%m-%Y")]]
                google_services.append_data_to_sheet("form" ,workbook.sheet1,
                                                     data_append_old)
                st.warning("La génération de devis n'est pas possible pour les familles avec un membre âgé de plus de 60 ans. Veuillez modifier la date de naissance si cela était une erreur.")

            if not all_fields_filled:
                st.error("Veuillez remplir tous les champs obligatoires, qui sont suivis d'un astérisque (*)")

            if phone_valid and email_valid and not member_over_60_found and all_fields_filled:
                st.session_state['file_ready_for_download'] = True

                # Assuming `config.devis_html` holds the URL to the HTML template
                response = requests.get(config.devis_html)
                if response.status_code == 200:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
                        tmp_file.write(response.content)
                    with open(tmp_file.name, 'r') as file:
                        html_template = file.read()

                else:
                    st.error(
                        "Un problème technique est survenu. Veuillez nous excuser pour ce désagrément et nous contacter par téléphone au 05 22 22 41 80 ou sur l'adresse email assistance.agecap@gmail.com .")

                # Extract family members' dates of birth and other details
                family_dobs = [dob for _, _, dob, _ in family_details]

                # Calculate premiums
                family_premiums = calculation.calculate_family_premiums(
                    family_dobs, primes, coefficients
                )

                # Sum premiums
                total_family_premiums = pd.DataFrame.from_dict(
                    calculation.sum_family_premiums(family_premiums)
                ).T

                # Generate the modified HTML content
                modified_html = doc_manip.insert_into_html(
                    html_template,
                    family_details,
                    total_family_premiums,
                    id_devis
                )

                # Save the modified HTML to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w") as tmp:
                    tmp.write(modified_html)
                    temp_file_path = tmp.name

                # Store the path in the session state to access it outside the form's scope
                st.session_state['temp_file_path'] = temp_file_path
                st.session_state['html_file'] = modified_html
                st.session_state.quote_calculated = True
                data_append_validated = [
                    [family_details[0][0], family_details[0][1], family_details[0][2].strftime("%d-%m-%Y"), email_address, phone_number,
                     medium, id_devis, datetime.datetime.today().strftime("%d-%m-%Y %H:%M:%S"), st.session_state.quote_calculated,nb_adultes,nb_enfants,"FR", "Non" ]]
                google_services.append_data_to_sheet("form", workbook.sheet1,
                                                     data_append_validated)
                # Use the path to your service account key file
                SERVICE_ACCOUNT_FILE = credentials
                # Folder ID where the file should be uploaded
                FOLDER_ID = config.folder_id  # Replace with your actual folder ID
                # Specify the filename and path of the PDF file to upload
                filename = f"devis_{id_devis}"
                filepath = st.session_state['temp_file_path']
                google_services.upload_file_to_google_drive(SERVICE_ACCOUNT_FILE, filename, filepath, FOLDER_ID,
                                                            mimetype='application/html')  # Clean up after download

                email_sender.send_email(st.session_state["email_address"],temp_file_path)
                switch_page("Devis")

    return