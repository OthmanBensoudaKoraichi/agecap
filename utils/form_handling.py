import datetime
import pandas as pd
import streamlit as st
from utils import calculation, function_check, doc_manip,google_services, config,data_loaders, hash_maker, email_sender
from streamlit_extras.switch_page_button import switch_page
import tempfile
import requests


def remove_family_member(index):
    st.session_state["family_count"] -= 1

    # Remove the specified family member
    for key in [f"relation_{index}", f"day_{index}", f"month_{index}", f"year_{index}"]:
        if key in st.session_state:
            del st.session_state[key]

    # Decrement the indices of the remaining family members
    for i in range(index + 1, st.session_state["family_count"] + 1):
        for key in ["relation", "day", "month", "year"]:
            old_key = f"{key}_{i}"
            new_key = f"{key}_{i - 1}"
            if old_key in st.session_state:
                st.session_state[new_key] = st.session_state[old_key]
                del st.session_state[old_key]

def process_form_submission(credentials,workbook):

    # Initialize session state for family members count
    if "family_count" not in st.session_state:
        st.session_state["family_count"] = 1

    if 'quote_calculated' not in st.session_state:
        st.session_state.quote_calculated = False

    if 'name_surname' not in st.session_state:
        st.session_state.name_surname = ""

    if 'enfant_25_detected' not in st.session_state:
        st.session_state.enfant_25_detected = False

    if 'conjoint_70_detected' not in st.session_state:
        st.session_state.conjoint_70_detected = False




    with st.form("insurance_form"):

        member_over_60_found = False
        member_over_70_found = False
        family_details = []
        all_fields_filled = True  # Assume all fields are initially filled
        phone_valid = True
        email_valid = True
        temp_file_path = None
        nb_adultes = 0
        nb_enfants = 0
        dates_naissance_conforme = True
        conjointe_age = 0
        souscripteur_age = 0


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
                    st.session_state.name_surname = first_name + "_" + surname


                day_options = list(range(1, 32))  # Possible day values
                month_options = config.months
                current_year = datetime.datetime.now().year
                year_options = list(range(current_year - 100, current_year + 1))  # Last 100 years

                # Using st.columns to align day, month, and year on the same line
                col1, col2, col3 = st.columns(3)
                with col1:
                    selected_day = st.selectbox(
                        "Jour de naissance",
                        options=day_options,
                        index=0 if f"day_{i}" not in st.session_state else day_options.index(
                            st.session_state[f"day_{i}"]),
                        key=f"day_{i}"
                    )
                with col2:
                    selected_month = st.selectbox(
                        "Mois de naissance",
                        options=month_options.keys(),
                        index=0 if f"month_{i}" not in st.session_state else list(month_options.keys()).index(
                            st.session_state[f"month_{i}"]),
                        key=f"month_{i}"
                    )
                with col3:
                    selected_year = st.selectbox(
                        "Année de naissance",
                        options=year_options,
                        index=25 if f"year_{i}" not in st.session_state else year_options.index(
                            st.session_state[f"year_{i}"]),
                        key=f"year_{i}"
                    )

                # Constructing the datetime object for the date of birth
                dob = datetime.datetime(year=selected_year, month=month_options[selected_month], day=selected_day)
                # Calculate age from dob and set flag if over 60
                age = calculation.calculate_age(dob)

                if relation_type == "Enfant" and age < 25:
                    nb_enfants += 1
                if not (relation_type == "Conjoint(e)" and age >= 70):
                    nb_adultes += 1
                if age >= 60:
                    member_over_60_found = True
                if age >= 70:
                    member_over_70_found = True

                if conjointe_age >= 60 and souscripteur_age >=60:
                    both_sixty = True

                # Append the details to the family_details list
                if i == 0:
                    family_details.append((first_name, surname, dob, relation_type))
                    souscripteur_age = age

                else:
                    if relation_type == "Conjoint(e)":
                        conjointe_age = age
                        if conjointe_age >= 70:
                            st.session_state.conjoint_70_detected = True

                    if relation_type == "Enfant" and age >= 25:
                        st.session_state.enfant_25_detected = True

                    if not ((relation_type == "Enfant" and age >= 25) or (relation_type == "Conjoint(e)" and age >= 70)):
                        family_details.append(("", "", dob, relation_type))


                # Button to remove this family member
                if i > 0:
                    if st.form_submit_button(f"Supprimer le membre {i}", type = "primary"):
                        remove_family_member(i)
                        st.rerun()
            # Display warning if the maximum number of family members is reached
            if i == 6:  # Check if this is the 7th family member (index 6)
                st.warning("Le maximum de 7 membres a été atteint.")


        # Button to add family members within the form
        st.form_submit_button(
            "Ajouter un membre de la famille",
            on_click=function_check.increment_family_count,
            type = "primary"
        )


        # Validate souscripteur details
        souscripteur_first_name = st.session_state.get("first_name_0", "")
        souscripteur_surname = st.session_state.get("surname_0", "")
        if not souscripteur_first_name or not souscripteur_surname:
            all_fields_filled = False

        if "email_address" not in st.session_state:
            st.session_state["email_address"] = None
        email_address = st.text_input("Adresse email *", key="email")
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


        amo = st.radio(
            "Bénéficiez-vous déjà de l'assurance maladie obligatoire auprès de la CNSS ?  *",
            ('Oui', 'Non', 'Je ne sais pas'), index = 2
        )
        # Select the medium, with index = 1 so that no medium is selected by default
        medium = st.radio(
            "Sur quel réseau social avez-vous vu notre formulaire? *",
            ('LinkedIn', 'Facebook', 'Instagram','Ne souhaite pas préciser'), index = 3
        )



        submit_button = st.form_submit_button("Calculer le devis", type = "primary")
        st.caption("Cela vous redirigera vers votre devis en quelques secondes.")


        if submit_button:
            if member_over_60_found == True and member_over_70_found == False:
                compagnie = "SANAD"
            else:
                compagnie = "AXA"
            st.write(souscripteur_age, member_over_60_found, member_over_70_found, compagnie)

            with st.spinner("Calcul du devis en cours. Veuillez patienter quelques secondes."):
                if 'id_devis' not in st.session_state:
                    st.session_state.id_devis = ''
                # Create id_devis
                id_devis = hash_maker.make_hash(family_details[0][0],family_details[0][1],family_details[0][1])
                st.session_state.id_devis = id_devis

                if phone_valid == False:
                    st.error("Format du numéro de téléphone invalide")
                if email_valid == False:
                    st.error("Format de l'adresse email invalide")



                # Final submit button is only enabled if all family members are below 60

                if souscripteur_age >= 70 and all_fields_filled:
                    data_append_old = [
                        [family_details[0][0], family_details[0][1], family_details[0][2].strftime("%d-%m-%Y"), email_address, phone_number,
                         medium, "Pas de devis", datetime.datetime.today().strftime("%d-%m-%Y %H:%M:%S"), "Oui" if st.session_state.quote_calculated else "Non",nb_adultes,nb_enfants,"FR", "Non", amo, "Aucune"]]
                    google_services.append_data_to_sheet("form" ,workbook.sheet1,
                                                         data_append_old)
                    # Delete all session states
                    for key in st.session_state.keys():
                        del st.session_state[key]
                    st.warning("Merci pour votre intérêt. Étant donné que ce produit est conçu pour des personnes de moins de 70 ans, nous vous recontacterons très bientôt avec une offre parfaitement adaptée à vos besoins.")

                if souscripteur_age < 18 and all_fields_filled:
                    data_append_young = [
                        [family_details[0][0], family_details[0][1], family_details[0][2].strftime("%d-%m-%Y"),
                         email_address, phone_number,
                         medium, "Pas de devis", datetime.datetime.today().strftime("%d-%m-%Y %H:%M:%S"),
                         "Oui" if st.session_state.quote_calculated else "Non", nb_adultes, nb_enfants, "FR", "Non",
                         amo, "Aucune"]]
                    google_services.append_data_to_sheet("form", workbook.sheet1,
                                                         data_append_young)
                    # Delete all session states
                    for key in st.session_state.keys():
                        del st.session_state[key]
                    st.warning(
                        "Merci pour votre intérêt. Étant donné que ce produit est conçu pour des personnes de plus de 18 ans, nous vous recontacterons très bientôt avec une offre parfaitement adaptée à vos besoins.")



                if not all_fields_filled:
                    st.error("Veuillez remplir tous les champs obligatoires, qui sont suivis d'un astérisque (*)")

                for _, _, dob, _ in family_details:
                    if dob > datetime.datetime.today():
                        # Use Streamlit's error function to display the error
                        # Make sure Streamlit is correctly set up for this
                        dates_naissance_conforme = False
                        st.error("Une date de naissance entrée n'est pas conforme. Veuillez vérifier les dates de naissance saisies.")
                        break  # Exit loop after finding the first future date, optional based on your needs

                if phone_valid and email_valid and souscripteur_age < 70 and all_fields_filled and dates_naissance_conforme:
                    st.session_state['file_ready_for_download'] = True

                    # Assuming `config.devis_html` holds the URL to the HTML template
                    response = requests.get(config.devis_html[compagnie])
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
                    relation_types = [relation_type for _, _, _, relation_type in family_details]

                    if compagnie == "AXA":
                        primes, coefficients = data_loaders.load_excel_data(config.primes_and_coef["AXA"], config.primes_and_coef["AXA"])
                        # Calculate premiums
                        family_premiums = calculation.calculate_family_premiums(
                            family_dobs,relation_types, primes, coefficients, compagnie
                        )

                    if compagnie == "SANAD":
                        primes = pd.read_excel(config.primes_and_coef["SANAD"], sheet_name="Sheet1")
                        # Calculate premiums
                        family_premiums = calculation.calculate_family_premiums(
                            family_dobs, primes, compagnie
                        )

                    # Sum premiums
                    total_family_premiums = pd.DataFrame.from_dict(
                        calculation.sum_family_premiums(family_premiums, compagnie)
                    ).T

                    # Generate the modified HTML content
                    modified_html = doc_manip.insert_into_html(
                        html_template,
                        family_details,
                        total_family_premiums,
                        id_devis,
                        compagnie
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
                         medium, id_devis, datetime.datetime.today().strftime("%d-%m-%Y %H:%M:%S"), "Oui" if st.session_state.quote_calculated else "Non",nb_adultes,nb_enfants,"FR", "Non", amo, compagnie]]
                    google_services.append_data_to_sheet("form", workbook.sheet1,
                                                         data_append_validated)
                    # Use the path to your service account key file
                    SERVICE_ACCOUNT_FILE = credentials
                    # Folder ID where the file should be uploaded
                    FOLDER_ID = config.folder_id  # Replace with your actual folder ID
                    # Specify the filename and path of the PDF file to upload
                    filename = f"devis_{id_devis}_{souscripteur_first_name}_{souscripteur_surname}"
                    # Read the HTML content from the temporary file
                    with open(st.session_state['temp_file_path'], 'r') as file:
                        devis_html_content = file.read()

                    # Convert HTML content to PDF and store the path in session state
                    st.session_state['pdf_path'] = doc_manip.convert_html_to_pdf(devis_html_content)
                    filepath = st.session_state['pdf_path']
                    google_services.upload_file_to_google_drive(SERVICE_ACCOUNT_FILE, filename, filepath, FOLDER_ID,
                                                                mimetype='application/pdf')  # Clean up after download

                    email_sender.send_email(st.session_state["email_address"],temp_file_path)
                    switch_page("Devis")

    return