import streamlit as st
from utils import config, style, chatbot, google_services
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page


# Set page config
st.set_page_config(page_icon=config.favicon, layout="wide", initial_sidebar_state="auto",
                   menu_items=None)

# Set style
# Set the layout of the app
style.set_app_layout(config.doodle)


## Display the HTML content directly in the Streamlit app
# Outside the form, check if the file is ready for download and then render the download button
if 'file_ready_for_download' in st.session_state and st.session_state['file_ready_for_download']:


   # if 'temp_file_path' in st.session_state:
        # Create a download button for the HTML file
      #  with open(st.session_state['temp_file_path'], 'rb') as file:
          #  btn = st.download_button(
              #  label="Télécharger le devis",
               # data=file,
              #  file_name="Devis_Agecap.html",
              #  mime="text/html",
               # type = "primary"
          #  )

    # Write next steps
    message = ("Votre devis est prêt. Vous pouvez le consulter sur cette page et vous avez reçu une copie par email.\n"
               "Pour continuer, veuillez remplir notre court questionnaire médical de 5 minutes. Vous avez également reçu une copie par email si vous souhaitez continuer la procédure ultérieurement (vérifiez dans votre boite de spams).")

    st.success(message)

    questionnaire_medical = st.button("Accéder au questionnaire médical",type = "primary")
    if questionnaire_medical:
        switch_page("questionnaire médical")
    contact = "Contactez-nous par téléphone au 05 22 22 41 80 ou sur l'adresse email assistance.agecap@gmail.com pour toute question."
    st.info(contact)

if ('quote_calculated' and 'html_file') in st.session_state:
    # If a quote has been calculated and an HTML file exists in the session state, display it
    components.html(st.session_state['html_file'], height=3000)
else:
    # If a quote hasn't been calculated or no HTML file exists, prompt the user to return to the form
    st.markdown("""
            <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-top: 10px; margin-bottom: 10px;">
                Veuillez retourner sur la page du formulaire afin de générer un devis.
            </div>
        """, unsafe_allow_html=True)
    go_to_form = st.button(label="Retourner au formulaire")
    if go_to_form:
        switch_page("Formulaire")

### GOOGLE CREDENTIALS ###
credentials_path = google_services.download_service_account_json(st.secrets["jsonkey_google"])
if credentials_path:
    workbook = google_services.setup_google_drive(credentials_path,"BDD clients opération commerciale")


### Chatbot ###

with st.container():
    # Set the style : Banner and hero
    chatbot.set_chatbot_style()
    # Initialize the chatbot
    qa, vectorstore = chatbot.initialize_chatbot(openaikey = st.secrets["openaikey"], pineconekey = st.secrets["pineconekey"], index_name = "agecap")

    # Handle chat interactions
    chatbot.handle_chat_interaction(qa, vectorstore, config.context, config.bot_avatar, config.user_avatar, workbook)
