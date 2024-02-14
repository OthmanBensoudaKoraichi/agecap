## Import libraries

import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Pinecone as lpn
from pinecone import Pinecone as pn
from utils import calculation, function_check, doc_manip, style, google_services
import datetime
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import ssl
import requests

ssl._create_default_https_context = ssl._create_unverified_context

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Your code to read Excel
primes = pd.read_excel('https://raw.githubusercontent.com/OthmanBensoudaKoraichi/agecap/master/files/sehassur_devis.xlsx')



# Use the columns to create a layout. Adjust the proportions as needed for your layout.
col1, col2, col3 = st.columns([1,2,1])  # This creates three columns, with the middle one being where the image will go.

# Place the image in the middle column to center it on the page
with col2:
    st.image("https://github.com/OthmanBensoudaKoraichi/agecap/blob/master/files/agecaplogo.png?raw=true")


# Path to your local image
doodle_path = "https://raw.githubusercontent.com/OthmanBensoudaKoraichi/agecap/master/files/doodle.png"

# Call the function to set the background image
style.set_bg_image(doodle_path, deploy = True)


scopes = ['https://www.googleapis.com./auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

# URL of the file on GitHub (ensure the token is kept secure and the repository is private)
file_url = 'https://raw.githubusercontent.com/OthmanBensoudaKoraichi/agecap/master/files/buoyant-apogee-411313-3fc58fa1faaa.json?token=GHSAT0AAAAAACM6C5JLAUIQVCJ7UMSGJG5GZOMH2BA'

# Local path to save the downloaded file
local_file_path = '/tmp/service_account.json'

# Download the file
response = requests.get(file_url)
if response.status_code == 200:
    with open(local_file_path, 'wb') as file:
        file.write(response.content)
    print("File downloaded successfully.")
else:
    print(f"Failed to download file: HTTP {response.status_code}")
    # Handle failure appropriately



creds = ServiceAccountCredentials.from_json_keyfile_name(local_file_path)

file = gspread.authorize(creds)
workbook = file.open("BDD clients opération commerciale")


css="""
<style>
    [data-testid="stForm"] {
        background:  #FFFFFF;
    }
</style>
"""
st.write(css, unsafe_allow_html=True)


# Initialize LangChain Chatbot and OpenAI Embeddings
OPENAI_API_KEY = st.secrets["openaikey"]
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.0
)
embed = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)

# Pinecone setup
pc = pn(api_key=st.secrets["pineconekey"])
index = pc.Index("agecap")

# Setup for vectorstore
vectorstore = lpn(index, embed, "text")


# Initialize RetrievalQA
qa = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
)

context = (
    "Vous êtes un courtier en assurances basé au Maroc, spécialisé dans les assurances maladies. "
    "Votre expertise en assurance maladie vous permet de donner des conseils avisés et personnalisés à vos clients, "
    "en vous appuyant sur votre vaste connaissance du domaine. "
    "Votre communication avec les clients doit être directe, cordiale et compréhensible, sans mentionner explicitement "
    "vos sources d'information. "
    "En cas de question dont la réponse dépasse votre champ de connaissances, "
    "il est crucial d'admettre de manière transparente que vous ne disposez pas de l'information demandée, "
    "tout en restant serviable et orienté vers la solution. "
    "Votre objectif est de répondre aux interrogations de manière aussi naturelle et personnelle que possible, "
    "comme si vous partagiez votre propre expertise sans faire référence à des documents externes. "
    "Voici la question de l'utilisateur : "
)



def main():
    # Display YouTube video
    video_url = "https://www.youtube.com/watch?v=ICVHhbXxjOw"

    with st.container():
        # Display a stylish and sophisticated banner
        style.embed_youtube_video(video_url, width=672, height=378)

        # Display a stylish and sophisticated banner
        st.markdown("""
            <style>
                .banner {
                    color: #fff;  /* White text color */
                    padding: 20px;  /* Padding inside the banner for spacing */
                    border-radius: 10px;  /* Rounded corners for a softer look */
                    background: linear-gradient(120deg, #6CB2E4 0%, #012B5C 100%);  /* Gradient background */
                    box-shadow: 0 4px 6px 0 rgba(0,0,0,0.2);  /* Subtle shadow for depth */
                    margin-top: 20px;  /* Margin at the top */
                    text-align: center;  /* Center the text */
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;  /* Modern, readable font */
                    font-size: 24px;  /* Slightly larger font size for impact */
                    font-weight: 500;  /* Medium font weight */
                }
            </style>
            <div class="banner">
                Remplissez notre formulaire et obtenez un devis en 1 clic !  
            </div>
        """, unsafe_allow_html=True)

    # Ajout d'une note sous la bannière
    st.markdown("""
        <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-top: 10px; margin-bottom: 10px;">
            <strong>Note importante :</strong> La tarification de votre devis est précisément ajustée en fonction de la <strong>date de naissance</strong> de chaque membre de la famille. Il est donc essentiel de remplir ces champs avec exactitude pour assurer une estimation adéquate de votre devis.
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state for family members count
    if "family_count" not in st.session_state:
        st.session_state["family_count"] = 1

    # Read table for the quote
    primes = pd.read_excel(
        "https://raw.githubusercontent.com/OthmanBensoudaKoraichi/agecap/master/files/sehassur_devis.xlsx",
        sheet_name="primes",
    )
    coefficients = pd.read_excel(
        "https://raw.githubusercontent.com/OthmanBensoudaKoraichi/agecap/master/files/sehassur_devis.xlsx",
        sheet_name="coefficients",
    )

    # Form for family members and communication preference
    with st.form("insurance_form"):
        member_over_60_found = False
        family_details = []
        all_fields_filled = True  # Assume all fields are initially filled
        phone_valid = True
        email_valid = True
        temp_file_path = None

        # Get quote number, which is the index of the last row filled
        all_values = workbook.sheet1.get_all_values()
        id_devis = f'AM_{len(all_values) + 1}'  # This gives  the index of the last row with data

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
                        f"Relation au souscripteur",
                        options=["Conjoint(e)", "Enfant"],
                        index=0 if i == 1 else 1,  # Default to Conjoint(e) for the first and Enfant thereafter
                        key=f"relation_{i}"
                    )

                first_name = st.text_input(f"Prénom {(i == 0) * '*'}", key=f"first_name_{i}")
                surname = st.text_input(f"Nom {(i == 0) * '*'}", key=f"surname_{i}")
                dob = st.date_input(
                    f"Date de naissance {(i == 0) * '*'}",
                    key=f"dob_{i}",
                    min_value=datetime.datetime.now() - datetime.timedelta(days=365.25 * 100),
                    format="DD-MM-YYYY",
                )


                family_details.append((first_name, surname, dob,relation_type))
                # Calculate age from dob and set flag if over 60
                age = calculation.calculate_age(dob)
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


        email_address = st.text_input("Adresse email du souscripteur *", key="email")
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
            "Sur quel medium avez-vous vu notre formulaire? *",
            ('LinkedIn', 'Facebook', 'Instagram','Ne souhaite pas préciser'), index = 3
        )

        submit_button = st.form_submit_button("Calculer le devis")

        if submit_button:
            if phone_valid == False:
                st.error("Format du numéro de téléphone invalide")
            if email_valid == False:
                st.error("Format de l'adresse email invalide")
            # Check if a medium has been selected
            if medium not in ('LinkedIn', 'Facebook', 'Instagram','Ne souhaite pas préciser'):
                st.error("La sélection d'un médium est obligatoire.")
                all_fields_filled = False
            # Final submit button is only enabled if all family members are below 60
            if member_over_60_found and all_fields_filled:
                st.warning("La génération de devis n'est pas possible pour les familles avec un membre âgé de plus de 60 ans. Veuillez rafraîchir la page et remplir le formulaire à nouveau si cela était une erreur.")
                data_append_old = ["Othman", "Some other value", "Another value"]
                google_services.append_data_to_sheet(workbook.sheet2, data_append_old)
            if not all_fields_filled:
                st.error("Veuillez remplir tous les champs obligatoires, qui sont suivis d'un astérisque (*)")



            if phone_valid and email_valid and not member_over_60_found and all_fields_filled:
                st.session_state['file_ready_for_download'] = True
                st.session_state[
                    'temp_file_path'] = temp_file_path  # Assuming `temp_file_path` holds the path to the generated file

                # Extract family members' dates of birth
                family_dobs = [dob for _, _, dob,_ in family_details]

                # Calculate premiums
                family_premiums = calculation.calculate_family_premiums(
                    family_dobs, primes, coefficients
                )

                # Sum premiums
                total_family_premiums = pd.DataFrame.from_dict(
                    calculation.sum_family_premiums(family_premiums)
                ).T

                import requests
                from docx import Document

                # URL of the .docx file on GitHub
                docx_url = 'https://raw.githubusercontent.com/OthmanBensoudaKoraichi/agecap/master/files/devis_agecap.docx'

                # Temporarily save the .docx file (adjust path as needed for your cloud environment)
                local_docx_path = '/tmp/devis_agecap_downloaded.docx'

                # Download the file
                response = requests.get(docx_url)
                if response.status_code == 200:
                    with open(local_docx_path, 'wb') as f:
                        f.write(response.content)
                    print("File downloaded successfully.")
                else:
                    print(f"Failed to download file: HTTP {response.status_code}")
                    exit()

                # Insert into word doc
                temp_file_path = doc_manip.insert_into_word_doc(
                    local_docx_path,
                    family_details,
                    total_family_premiums,id_devis
                )

                # Store the path in the session state to access it outside the form's scope
                st.session_state['temp_file_path'] = temp_file_path

        # Outside the form, check if the file is ready for download and then render the download button
    if 'file_ready_for_download' in st.session_state and st.session_state['file_ready_for_download']:
        if 'temp_file_path' in st.session_state and os.path.exists(st.session_state['temp_file_path']):
            # Display success message
            st.success("Votre devis est prêt à être téléchargé.")

            # Create a download button for the PDF, now outside the form
            with open(st.session_state['temp_file_path'], 'rb') as file:
                btn = st.download_button(
                    label="Télécharger le devis",
                    data=file,
                    file_name="Devis_Agecap.docx",
                    mime="application/docx"
                )

            if btn:
                data_append_validated = ["Othman", "Some other value", "Another value"]
                google_services.append_data_to_sheet(workbook.sheet1, data_append_validated)
                # Use the path to your service account key file
                SERVICE_ACCOUNT_FILE = local_file_path
                # Folder ID where the file should be uploaded
                FOLDER_ID = '1jzqRv_SvUz1EkeV0AnlgY00PaTKhXjm4'  # Replace with your actual folder ID
                # Specify the filename and path of the PDF file to upload
                filename = f"devis_{id_devis}"
                filepath = st.session_state['temp_file_path']
                google_services.upload_file_to_google_drive(SERVICE_ACCOUNT_FILE, filename, filepath, FOLDER_ID,
                                                            mimetype='application/pdf')            # Clean up after download
                os.remove(st.session_state['temp_file_path'])
                del st.session_state['temp_file_path']



    ### Chatbot
    with st.container():
        # Display a stylish and sophisticated banner
        # Création de deux colonnes : une pour l'image et une pour la bannière
        colbot1, colbot2 = st.columns([1, 3], gap = 'small')  # Ajustez les proportions selon vos besoins

        # Dans la première colonne, ajoutez votre image
        with colbot1:
            st.image("https://github.com/OthmanBensoudaKoraichi/agecap/blob/master/files/agecap_hero.png?raw=true", width=150)  # Ajustez le chemin et la largeur selon vos besoins

        # In the second column, place your banner
        with colbot2:
            st.markdown("""
                <style>
                    .speech-bubble {
                        position: relative;
                        background: #6CB2E4;
                        border-radius: .4em;
                        color: #fff;
                        padding: 20px;
                        text-align: center;
                        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                        font-size: 18px;
                        font-weight: 500;
                        margin-bottom: 20px;
                    }

                    .speech-bubble:after {
                        content: '';
                        position: absolute;
                        top: 0;
                        left: -20px;
                        width: 0;
                        height: 0;
                        border: 10px solid transparent;
                        border-right-color: #6CB2E4;
                        border-left: 0;
                        border-top: 0;
                        margin-top: 5px;
                        margin-left: -10px;
                    }
                </style>
                <div class="speech-bubble">
                    Posez une question sur notre assurance maladie complémentaire et recevez une réponse instantanément.
                </div>
            """, unsafe_allow_html=True)

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            st.info(f"{message['role']}: {message['content']}")

        # Check if the user has already sent 10 messages
        if len(st.session_state.messages) >= 10:
            st.warning("Pour plus de questions, veuillez appeler notre assistance au 05 22 22 41 80.")
        else:
            query = st.chat_input("Posez votre question", key="chatbot_input")

            if query:
                # Display user message in chat message container
                st.chat_message(name = "Vous",avatar = 'https://github.com/OthmanBensoudaKoraichi/agecap/blob/master/files/user_avatar.png?raw=true').markdown(query)
                # Add user message to chat history
                st.session_state.messages.append({"role": "Vous", "content": query})

                with st.spinner("Veuillez patienter quelques secondes"):
                    vectorstore.similarity_search(query, k=3)

                    # Combine them with a newline character which often signifies a new paragraph or a separation of ideas
                    combined_input = context + "\n" + query
                    response = qa.run(combined_input)

                    with st.chat_message(name = "Assistant Agecap",avatar='https://github.com/OthmanBensoudaKoraichi/agecap/blob/master/files/agecaplogosmall.png?raw=true'):
                        st.markdown(response)
                    # Add ai response to chat history
                st.session_state.messages.append({"role": "Assistant Agecap", "content": response})

                # Prepare the data to be appended
                # Include other details as required, for example, chat history
                # Concatenate chat messages into a single string or format as needed
                chat_history = "--------".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])

                # Append the data to the sheet
                google_services.append_data_to_sheet(workbook.sheet1,[chat_history])


if __name__ == "__main__":
    main()
