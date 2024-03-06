import streamlit as st
from utils import chatbot, google_services, config,style
from streamlit_extras.switch_page_button import switch_page
import datetime
import pandas as pd
import tempfile

# Set the layout of the app
st.set_page_config(page_icon=config.favicon, layout="wide", initial_sidebar_state="auto",
                   menu_items=None)
style.set_app_layout(config.doodle)

### GOOGLE CREDENTIALS ###
credentials_path = google_services.download_service_account_json(st.secrets["jsonkey_google"])
if credentials_path:
    workbook = google_services.setup_google_drive(credentials_path,"BDD clients opération commerciale")



### Program ###

if 'quote_calculated' not in st.session_state:
    st.session_state.quote_calculated = False

if 'come_after_email' not in st.session_state:
    st.session_state.come_after_email = False

if 'id_devis' not in st.session_state:
    st.session_state.id_devis = None


# Formulaire pour entrer le numéro de devis si celui-ci n'a pas encore été calculé
if st.session_state.quote_calculated == False:
    with st.form(key="numéro_de_devis"):
        st.session_state.come_after_email = True
        num_devis = st.text_input("#### Entrez le numéro de devis que vous avez obtenu par email (Exemple : b332a-AM).").replace(" ", "")
        submit_num_devis = st.form_submit_button("Valider")

    # Récupération des numéros de devis depuis la 7ème colonne après avoir soumis le formulaire pour éviter les appels inutiles à l'API
    if submit_num_devis:
        st.session_state.id_devis = num_devis
        list_quote_numbers = workbook.sheet1.col_values(7)

        if num_devis in list_quote_numbers:
            # Trouver l'indice de la ligne où se trouve le numéro de devis (ajouter 1 car l'indexation commence à 1 dans la feuille de calcul)
            row_index = list_quote_numbers.index(num_devis) + 1
            # Récupérer le nom dans la 2ème colonne pour cette ligne
            prenom = workbook.sheet1.cell(row_index,
                                       1).value
            nom = workbook.sheet1.cell(row_index,
                                       2).value  # Assurez-vous que l'indexation des colonnes correspond à votre feuille
            st.success(f"Numéro de devis trouvé sous le nom de {prenom + ' ' + nom.upper()}.")
            st.session_state.quote_calculated = True
        else:
            st.error(
                "Numéro de devis introuvable. Contactez-nous par téléphone au 05 22 22 41 80 ou sur l'adresse email assistance.agecap@gmail.com pour toute question.")


# Si le devis a été calculé ou après la soumission du formulaire de devis, exécutez le reste
if st.session_state.quote_calculated == True:
    # Boutons pour changer de page
    go_to_quote = st.button(label="Retourner au devis")
    if go_to_quote:
        switch_page("Devis")

    # Style
    style.banner_questionnaire_medical()

    # Utiliser st.radio pour la sélection initiale
    offre = st.radio("**À quelle offre voudriez-vous souscrire ?**", ("Essentielle", "Optimale","Intégrale"), index=2)
    choix = st.radio("**Voulez-vous également assurer votre conjoint(e) ?**", ("Oui", "Non"),index=1)

    # Mettre à jour l'état de session basé sur le choix
    # Cela est fait avant d'entrer dans le formulaire pour éviter des modifications après l'instanciation
    if choix == "Non":
        st.session_state.assurer_conjoint = False
    else:
        st.session_state.assurer_conjoint = True


    # Création d'un formulaire
    with st.form(key='medical_form'):
        # Afficher les colonnes en fonction du choix
        if st.session_state.assurer_conjoint:
            col1, col2 = st.columns(2)
        else:
            col1 = st.columns(1)[0]  # Utiliser le premier élément de la liste retournée par st.columns(1)
            col2 = None

        with col1:
            st.markdown("**Souscripteur**")
            # Starting the questionnaire
            emploi = st.text_input("**Quel emploi occupez-vous actuellement ?**",key = "emploi")
            assurance_complementaire = st.radio("**Bénéficiez-vous d'une assurance maladie complémentaire auprès d'une autre compagnie ?**",
                                 ["Oui", "Non"],key = "ass_comp")
            assurance_complementaire_si_oui = st.text_input("**Si oui, auprès de quelle compagnie? Depuis quand ?**",key = "ass_comp_si_oui")


            traitement_medical = st.radio("**Suivez-vous un traitement médical ?**", ["Oui", "Non"],key = "trait_med")
            traitement_si_oui = st.text_input("**Si oui, lesquels ?**",key = "traitement_si_oui")


            maladie_grave = st.radio("**Avez-vous été atteint de maladie grave ou chronique ?**", ["Oui", "Non"],key = "maladie_grave")

            st.write("**Si oui, lesquelles ?**")
            # Définition des variables en fonction de l'état des cases à cocher
            hta = "oui" if st.checkbox("HTA",key = "hta") else "non"
            cholesterol= "oui" if st.checkbox("Cholestérol",key = "chol") else "non"
            cardiopathie = "oui" if st.checkbox("Cardiopathie", key = "cardio") else "non"
            oncologie = "oui" if st.checkbox("Oncologie", key = "onc") else "non"
            diabete = "oui" if st.checkbox("Diabète", key = "diab") else "non"

            # Définition d'un champ de saisie de texte pour les autres conditions
            autres_maladies = st.text_input("**Autres à préciser**",key = "autres_maladies")
            # Additional questions
            arret_travail = st.radio("**Êtes-vous en arrêt de travail ?**", ["Oui", "Non"],key = "arret_travail")
            arret_travail_si_oui = st.text_input("**Si oui, depuis quand ? Pour quel motif ?**",key = "arret_travail_si_oui")

            operations_chirurgicales = st.radio("**Avez-vous subi des opérations chirurgicales ?**", ["Oui", "Non"],key = "op_chir")
            operations_chirurgicales_si_oui = st.text_input("**Si oui, lesquelles ? Suites éventuelles ?**",key = "op_chir_si_oui")

            # Infirmité and Pension d'invalidité
            infirmite = st.radio("**Êtes-vous atteint d'une infirmité ?**", ["Oui", "Non"],key = "infirmite")
            infirmite_si_oui = st.text_input("Si oui, laquelle ?",key = "infirmite_si_oui")

            pension_invalidite = st.radio("**Êtes-vous titulaire d'une pension d'invalidité ?**", ["Oui", "Non"],key = "pens_inv")
            pension_invalidite_si_oui = st.text_input("**A quel titre ? A quel taux ?**",key = "pension_inv_si_oui")

            # Date d'entrée en invalidité
            invalidite_date = st.text_input("**Date d'entrée en invalidité ?**",key = "invalidite_date")

            # Risques professionnels
            risque_pro = st.radio(
                "**Êtes-vous exposé à un danger dans l'exercice de votre profession ou avez-vous l'intention de vous engager dans des activités suivantes ? "
                "[Aviation, parachutisme, parapente, delta-plane, sports mécaniques, plongée, escalade, spéléologie ou tout autre activité jugée dangereuse]**",
                ["Oui", "Non"],key = "risque_pro")

            # Historique médical
            historique_medical = st.radio(
                "**Avez-vous déjà eu ou reçu un avis médical ou un traitement pour l'un des problèmes suivants ? [Douleur thoracique, hypertension artérielle, crise cardiaque, accident vasculaire cérébral, diabète, troubles cardiaque, maladies vasculaires, Cancer, mélanome, tumeur ou croissance de toute sorte, Gastro-intestinal, génito-urinaire, respiratoire, oreilles, yeux, épilepsie, neurologique, psychiatrique, rénal, troubles hépatiques, métaboliques et endocriniens, Affections articulaires, des membres ou des os, maladies auto-immunes, maladies infectieuses Hépatite B ou C, VIH, maladie de Lyme, tuberculose, dépendance à l'alcool ou aux drogues**",
                ["Oui", "Non"],key = "hist_med")

            # Antécédents familiaux
            antecedents_familiaux = st.radio(
                "**Est-ce que votre mère biologique, votre père ou toute sœur ou frère a été diagnostiqué avant l'âge de 60 ans avec l'un de ce qui suit ? [Cancer, crise cardiaque, accident vasculaire cérébral, maladie de Huntington ou toute autre maladie héréditaire]**",["Oui", "Non"],key = "ant_fam")

            # Défaut de la vue et Grossesse
            defaut_vue = st.radio("**Êtes-vous atteint d'un défaut de la vue ?**", ["Oui", "Non"],key = "def_vue")
            grossesse = st.radio("**Êtes-vous en état de grossesse ?**", ["Oui", "Non"],key = "grossesse")
            grossesse_si_oui = st.number_input("**Si oui, de combien de mois ?**", min_value=0, max_value=9,key = "grossesse_si_oui")

            # Physical characteristics
            taille =  st.number_input("**Taille (cm)**", min_value=0, max_value=250, key="height")
            poids = st.number_input("**Poids (kg)**", min_value=0, max_value=300, key="weight")

            st.write("#### Indiquez pour chaque enfant les infirmités, les maladies antérieures, ainsi que les opérations chirurgicales.")

            # Création de 5 colonnes
            cols = st.columns(5)

            # Initialisation du dictionnaire pour les informations sur les enfants
            informations_enfants = {}

            # Utilisation d'une boucle pour générer les champs pour le nombre d'enfants sélectionné
            for i in range(5):
                with cols[i]:
                    st.markdown(f"### Enfant {i + 1}")
                    prenom = st.text_input("**Prénom**", key=f"child_{i + 1}_name")
                    etat_de_sante_actuel = st.text_input("**État de santé actuel**", key=f"child_{i + 1}_current_health")
                    date_de_naissance = st.text_input("**Date de naissance (Jour/Mois/Année)**",
                                                      key=f"child_{i + 1}_birth_date")
                    infirmities = st.text_input("**Infirmités**", key=f"child_{i + 1}_infirmities")
                    maladies_anterieures = st.text_input("**Maladies antérieures**", key=f"child_{i + 1}_previous_diseases")
                    operations_chirurgicales = st.text_input("**Opérations chirurgicales**", key=f"child_{i + 1}_surgeries")

                    # Ajout des informations de l'enfant actuel au dictionnaire
                    informations_enfants[f"enfant_{i + 1}"] = {
                        "prenom_enfant": prenom,
                        "etat_de_sante_actuel_enfant": etat_de_sante_actuel,
                        "date_de_naissance_enfant": date_de_naissance,
                        "infirmities_enfant": infirmities,
                        "maladies_anterieures_enfant": maladies_anterieures,
                        "operations_chirurgicales_enfant": operations_chirurgicales
                    }

        if st.session_state.assurer_conjoint and col2 is not None:
            with col2:
                st.markdown("**Conjoint(e)**")
                # Starting the questionnaire
                emploi_conj = st.text_input("**Quel emploi occupez-vous actuellement ?**")
                assurance_complementaire_conj = st.radio(
                    "**Bénéficiez-vous d'une assurance maladie complémentaire auprès d'une autre compagnie ?**",
                    ["Oui", "Non"])
                assurance_complementaire_si_oui_conj = st.text_input("**Si oui, auprès de quelle compagnie ? Depuis quand ?**")

                traitement_medical_conj = st.radio("**Suivez-vous un traitement médical **", ["Oui", "Non"])
                traitement_si_oui_conj = st.text_input("**Si oui, lesquels ?**")

                maladie_grave_conj = st.radio("**Avez-vous été atteint de maladie grave ou chronique ?**", ["Oui", "Non"])

                st.write("**Si oui, lesquelles ?**")
                # Définition des variables en fonction de l'état des cases à cocher
                hta_conj = "oui" if st.checkbox("HTA") else "non"
                cholesterol_conj = "oui" if st.checkbox("Cholestérol") else "non"
                cardiopathie_conj = "oui" if st.checkbox("Cardiopathie") else "non"
                oncologie_conj = "oui" if st.checkbox("Oncologie") else "non"
                diabete_conj = "oui" if st.checkbox("Diabète") else "non"

                # Définition d'un champ de saisie de texte pour les autres conditions
                autres_maladies_conj = st.text_input("**Autres à préciser**")
                # Additional questions
                arret_travail_conj = st.radio("**Êtes-vous en arrêt de travail ?**", ["Oui", "Non"])
                arret_travail_si_oui_conj = st.text_input("**Si oui, depuis quand? Pour quel motif ?**")

                operations_chirurgicales_conj = st.radio("**Avez-vous subi des opérations chirurgicales ?**", ["Oui", "Non"])
                operations_chirurgicales_si_oui_conj = st.text_input("**Si oui, lesquelles? Suites éventuelles ?**")

                # Infirmité and Pension d'invalidité
                infirmite_conj = st.radio("**Êtes-vous atteint d'une infirmité ?**", ["Oui", "Non"])
                infirmite_si_oui_conj = st.text_input("Si oui, laquelle ?")

                pension_invalidite_conj = st.radio("**Êtes-vous titulaire d'une pension d'invalidité ?**", ["Oui", "Non"])
                pension_invalidite_si_oui_conj = st.text_input("**A quel titre? A quel taux ?**")

                # Date d'entrée en invalidité
                invalidite_date_conj = st.text_input("**Date d'entrée en invalidité ?**")

                # Risques professionnels
                risque_pro_conj = st.radio(
                    "**Êtes-vous exposé à un danger dans l'exercice de votre profession ou avez-vous l'intention de vous engager dans des activités suivantes ? "
                    "[Aviation, parachutisme, parapente, delta-plane, sports mécaniques, plongée, escalade, spéléologie ou tout autre activité jugée dangereuse]**",
                    ["Oui", "Non"])

                # Historique médical
                historique_medical_conj = st.radio(
                    "**Avez-vous déjà eu ou reçu un avis médical ou un traitement pour l'un des problèmes suivants ? [Douleur thoracique, hypertension artérielle, crise cardiaque, accident vasculaire cérébral, diabète, troubles cardiaque, maladies vasculaires, Cancer, mélanome, tumeur ou croissance de toute sorte, Gastro-intestinal, génito-urinaire, respiratoire, oreilles, yeux, épilepsie, neurologique, psychiatrique, rénal, troubles hépatiques, métaboliques et endocriniens, Affections articulaires, des membres ou des os, maladies auto-immunes, maladies infectieuses Hépatite B ou C, VIH, maladie de Lyme, tuberculose, dépendance à l'alcool ou aux drogues**",
                    ["Oui", "Non"])

                # Antécédents familiaux
                antecedents_familiaux_conj = st.radio(
                    "**Est-ce que votre mère biologique, votre père ou toute sœur ou frère a été diagnostiqué avant l'âge de 60 ans avec l'un de ce qui suit ? [Cancer, crise cardiaque, accident vasculaire cérébral, maladie de Huntington ou toute autre maladie héréditaire]**",
                    ["Oui", "Non"])

                # Défaut de la vue et Grossesse
                defaut_vue_conj = st.radio("**Êtes-vous atteint d'un défaut de la vue ?**", ["Oui", "Non"])
                grossesse_conj = st.radio("**Êtes-vous en état de grossesse ?**", ["Oui", "Non"])
                grossesse_si_oui_conj = st.number_input("**Si oui, de combien de mois ?**", min_value=0, max_value=9)

                # Physical characteristics
                taille_conj = st.number_input("**Taille (cm)**", min_value=0, max_value=250, key="height_conj")
                poids_conj = st.number_input("**Poids (kg)**", min_value=0, max_value=300, key="weight_conj")

        # Bouton de soumission du formulaire
        submit_button = st.form_submit_button("Soumettre")

    if submit_button:
        st.success("Merci d'avoir rempli le questionnaire ! Nous l'avons bien reçu et nous vous contacterons dans les plus brefs délais. Contactez-nous par téléphone au 05 22 22 41 80 ou sur l'adresse email assistance.agecap@gmail.com pour toute question.")
        # Initialisation du dictionnaire pour les informations sur le souscripteur
        data_souscripteur = {
            "offre" : offre,
            "Quel emploi occupez-vous actuellement?": emploi,
            "Bénéficiez-vous d'une assurance maladie complémentaire auprès d'une autre compagnie?": assurance_complementaire,
            "Si oui, auprès de quelle compagnie? Depuis quand?": assurance_complementaire_si_oui,
            "Suivez-vous un traitement médical?": traitement_medical,
            "Si oui, lesquels?": traitement_si_oui,
            "Avez-vous été atteint de maladie grave ou chronique ?": maladie_grave,
            "HTA": hta,
            "Cholestérol": cholesterol,
            "Cardiopathie": cardiopathie,
            "Oncologie": oncologie,
            "Diabète": diabete,
            "Autres à préciser": autres_maladies,
            "Êtes-vous en arrêt de travail?": arret_travail,
            "Si oui, depuis quand? Pour quel motif?": arret_travail_si_oui,
            "Avez-vous subi des opérations chirurgicales?": operations_chirurgicales,
            "Si oui, lesquelles? Suites éventuelles?": operations_chirurgicales_si_oui,
            "Êtes-vous atteint d'une infirmité?": infirmite,
            "Si oui, laquelle ?": infirmite_si_oui,
            "Êtes-vous titulaire d'une pension d'invalidité?": pension_invalidite,
            "A quel titre? A quel taux?": pension_invalidite_si_oui,
            "Date d'entrée en invalidité?": invalidite_date,
            "Êtes-vous exposé à un danger dans l'exercice de votre profession ou avez-vous l'intention de vous engager dans des activités suivantes? [Aviation, parachutisme, parapente, delta-plane, sports mécaniques, plongée, escalade, spéléologie ou tout autre activité jugée dangereuse]": risque_pro,
            "Avez-vous déjà eu ou reçu un avis médical ou un traitement pour l'un des problèmes suivants ? [Douleur thoracique, hypertension artérielle, crise cardiaque, accident vasculaire cérébral, diabète, troubles cardiaque, maladies vasculaires, Cancer, mélanome, tumeur ou croissance de toute sorte, Gastro-intestinal, génito-urinaire, respiratoire, oreilles, yeux, épilepsie, neurologique, psychiatrique, rénal, troubles hépatiques, métaboliques et endocriniens, Affections articulaires, des membres ou des os, maladies auto-immunes, maladies infectieuses Hépatite B ou C, VIH, maladie de Lyme, tuberculose, dépendance à l'alcool ou aux drogues": historique_medical,
            "Est-ce que votre mère biologique, votre père ou toute sœur ou frère a été diagnostiqué avant l'âge de 60 ans avec l'un de ce qui suit? [Cancer, crise cardiaque, accident vasculaire cérébral, maladie de Huntington ou toute autre maladie héréditaire]": antecedents_familiaux,
            "Êtes-vous atteint d'un défaut de la vue?": defaut_vue,
            "Êtes-vous en état de grossesse?": grossesse,
            "Si oui, de combien de mois?": grossesse_si_oui,
            "Taille (cm)": taille,
            "Poids (kg)": poids
        }

        # Convertir les dictionnaires en DataFrame
        df_informations_enfants = pd.DataFrame(informations_enfants).transpose()
        df_data_souscripteur = pd.DataFrame([data_souscripteur]).transpose()

        if st.session_state.assurer_conjoint == True:

            # Initialisation du dictionnaire pour les informations sur le conjoint
            data_conjoint = {
                "Quel emploi occupe votre conjoint actuellement?": emploi_conj,
                "Bénéficie-t-il/elle d'une assurance maladie complémentaire auprès d'une autre compagnie?": assurance_complementaire_conj,
                "Si oui, auprès de quelle compagnie? Depuis quand?": assurance_complementaire_si_oui_conj,
                "Suit-il/elle un traitement médical?": traitement_medical_conj,
                "Si oui, lesquels?": traitement_si_oui_conj,
                "A-t-il/elle été atteint de maladie grave ou chronique ?": maladie_grave_conj,
                "HTA": hta_conj,
                "Cholestérol": cholesterol_conj,
                "Cardiopathie": cardiopathie_conj,
                "Oncologie": oncologie_conj,
                "Diabète": diabete_conj,
                "Autres à préciser": autres_maladies_conj,
                "Êtes-vous en arrêt de travail?": arret_travail_conj,
                "Si oui, depuis quand? Pour quel motif?": arret_travail_si_oui_conj,
                "A-t-il/elle subi des opérations chirurgicales?": operations_chirurgicales_conj,
                "Si oui, lesquelles? Suites éventuelles?": operations_chirurgicales_si_oui_conj,
                "Êtes-vous atteint d'une infirmité?": infirmite_conj,
                "Si oui, laquelle ?": infirmite_si_oui_conj,
                "Êtes-vous titulaire d'une pension d'invalidité?": pension_invalidite_conj,
                "A quel titre? A quel taux?": pension_invalidite_si_oui_conj,
                "Date d'entrée en invalidité?": invalidite_date_conj,
                "Êtes-vous exposé à un danger dans l'exercice de votre profession ou avez-vous l'intention de vous engager dans des activités suivantes? [Aviation, parachutisme, parapente, delta-plane, sports mécaniques, plongée, escalade, spéléologie ou tout autre activité jugée dangereuse]": risque_pro_conj,
                "A-t-il/elle déjà eu ou reçu un avis médical ou un traitement pour l'un des problèmes suivants ? [Douleur thoracique, hypertension artérielle, crise cardiaque, accident vasculaire cérébral, diabète, troubles cardiaque, maladies vasculaires, Cancer, mélanome, tumeur ou croissance de toute sorte, Gastro-intestinal, génito-urinaire, respiratoire, oreilles, yeux, épilepsie, neurologique, psychiatrique, rénal, troubles hépatiques, métaboliques et endocriniens, Affections articulaires, des membres ou des os, maladies auto-immunes, maladies infectieuses Hépatite B ou C, VIH, maladie de Lyme, tuberculose, dépendance à l'alcool ou aux drogues]": historique_medical_conj,
                "Est-ce que votre mère biologique, votre père ou toute sœur ou frère a été diagnostiqué avant l'âge de 60 ans avec l'un de ce qui suit? [Cancer, crise cardiaque, accident vasculaire cérébral, maladie de Huntington ou toute autre maladie héréditaire]": antecedents_familiaux_conj,
                "Êtes-vous atteint d'un défaut de la vue?": defaut_vue_conj,
                "Êtes-vous en état de grossesse?": grossesse_conj,
                "Si oui, de combien de mois?": grossesse_si_oui_conj,
                "Taille (cm)": taille_conj,
                "Poids (kg)": poids_conj
            }


            df_data_conjoint = pd.DataFrame([data_conjoint]).transpose()

        # Assuming df_informations_enfants, df_data_souscripteur, and df_data_conjoint are defined somewhere above this code

        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmpfile:
            with pd.ExcelWriter(tmpfile.name, engine='xlsxwriter') as writer:
                df_informations_enfants.to_excel(writer, sheet_name='Enfants', index=True)
                df_data_souscripteur.to_excel(writer, sheet_name='Souscripteur', index=True)

                if st.session_state.get('assurer_conjoint', False):  # Safely accessing 'assurer_conjoint'
                    df_data_conjoint.to_excel(writer, sheet_name='Conjoint(e)', index=True)

            # Now that the file has been created and data written to it, set the path in session state
            st.session_state['temp_file_path'] = tmpfile.name

        # Now you can safely access st.session_state['temp_file_path'] as it has been initialized
        filepath = st.session_state['temp_file_path']

        # Use the path to your service account key file
        SERVICE_ACCOUNT_FILE = credentials_path
        # Folder ID where the file should be uploaded
        FOLDER_ID = config.folder_id  # Replace with your actual folder ID
        # Specify the filename for the upload
        filename = f"questionnaire_medical_{st.session_state.id_devis}.xlsx"

        # Proceed to upload the file
        google_services.upload_file_to_google_drive(SERVICE_ACCOUNT_FILE, filename, filepath, FOLDER_ID,
                                                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')  # Specify the correct MIME type for an Excel file
        if st.session_state.come_after_email:
            status = "Oui après relance"
        else:
            status = "Oui avant relance"

        google_services.append_questionnaire_status(workbook.sheet1, status,st.session_state.id_devis )

### Chatbot ###

with st.container():
    # Set the style : Banner and hero
    chatbot.set_chatbot_style()
    # Initialize the chatbot
    qa, vectorstore = chatbot.initialize_chatbot(openaikey = st.secrets["openaikey"], pineconekey = st.secrets["pineconekey"], index_name = "agecap")

    # Handle chat interactions
    chatbot.handle_chat_interaction(qa, vectorstore, config.context, config.bot_avatar, config.user_avatar, workbook)
