import datetime
import pandas as pd
import streamlit as st
from utils import calculation, function_check, doc_manip,google_services, config,data_loaders, hash_maker, email_sender
from streamlit_extras.switch_page_button import switch_page
import tempfile


def process_form_submission(credentials,workbook):

    primes, coefficients = data_loaders.load_excel_data(config.primes_and_coef, config.primes_and_coef)
    # Initialize session state for family members count
    if "family_count" not in st.session_state:
        st.session_state["family_count"] = 1

    if 'already_has_input' not in st.session_state:
        st.session_state.already_has_input = False


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
        for i in range(st.session_state["family_count"]):
            expanded = True  # Expand all by default

            # Adjusting member labels based on index
            if i == 0:
                member_label = "Souscripteur (Vous)"
                relation_type = '/'
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

                first_name = st.text_input(f"Prénom {(i == 0) * '*'}", key=f"first_name_{i}")
                surname = st.text_input(f"Nom de famille {(i == 0) * '*'}", key=f"surname_{i}")
                dob = st.date_input(
                    f"Date de naissance {(i == 0) * '*'}",
                    key=f"dob_{i}",
                    min_value=datetime.datetime.now() - datetime.timedelta(days=365.25 * 100),
                    format="DD-MM-YYYY"
                )


                family_details.append((first_name, surname, dob,relation_type))
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
                st.session_state.id_devis = None
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
                google_services.append_data_to_sheet("form", st.session_state.already_has_input, workbook.sheet1,
                                                     data_append_old)
                st.warning("La génération de devis n'est pas possible pour les familles avec un membre âgé de plus de 60 ans. Veuillez rafraîchir la page et remplir le formulaire à nouveau si cela était une erreur.")

            if not all_fields_filled:
                st.error("Veuillez remplir tous les champs obligatoires, qui sont suivis d'un astérisque (*)")

            if phone_valid and email_valid and not member_over_60_found and all_fields_filled:
                st.session_state['file_ready_for_download'] = True

                html_template_path = '/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/devis_agecap.html'
                with open(html_template_path, 'r') as file:
                    html_template = file.read()

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
                st.session_state.already_has_input = True
                data_append_validated = [
                    [family_details[0][0], family_details[0][1], family_details[0][2].strftime("%d-%m-%Y"), email_address, phone_number,
                     medium, id_devis, datetime.datetime.today().strftime("%d-%m-%Y %H:%M:%S"), st.session_state.already_has_input,nb_adultes,nb_enfants,"FR", "Non" ]]
                google_services.append_data_to_sheet("form", st.session_state.already_has_input, workbook.sheet1,
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

                email_sender.send_email()
                switch_page("Devis")

    return