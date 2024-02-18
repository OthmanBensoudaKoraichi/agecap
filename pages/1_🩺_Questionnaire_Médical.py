import streamlit as st
from utils import chatbot, google_services, config,style
from streamlit_extras.switch_page_button import switch_page

# Set the layout of the app
style.set_app_layout(config.doodle)



# Boutons pour changer de page
go_to_form = st.button(label="Retourner au formulaire")
if go_to_form:
    switch_page("Formulaire")

go_to_quote = st.button(label="Retourner au devis")
if go_to_quote:
    switch_page("Devis")

# Titre de l'application
st.title("Questionnaire Médical")

# Utiliser st.radio pour la sélection initiale
choix = st.radio("Voulez-vous également assurer votre conjoint(e) ?", ("Oui", "Non"),index=1)

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
        st.markdown("**Assuré(e)**")
        # Questions pour l'assuré(e)...

    if st.session_state.assurer_conjoint and col2 is not None:
        with col2:
            st.markdown("**Conjoint**")
            # Questions pour le conjoint...

    # Bouton de soumission du formulaire
    submit_button = st.form_submit_button("Soumettre")

if submit_button:
    st.success("Merci d'avoir rempli le questionnaire.")

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
