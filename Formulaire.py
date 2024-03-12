# Import libraries
import streamlit as st
from utils import style, google_services, config, chatbot, form_handling

# Main function
def main():

    ### STYLE ###
    st.set_page_config(page_icon=config.favicon, layout="centered", initial_sidebar_state="auto",
                       menu_items=None)

    # Set the layout of the app
    style.display_chat_indication_message()
    style.set_app_layout(config.doodle)

    style.set_label_text_color()

    style.set_text_color()

    # Create columns and place logo
    col1, col2, col3 = style.create_columns()
    style.place_logo(col2,config.agecap_logo)

    with st.container():
        # Display a stylish and sophisticated banner
        style.embed_vimeo_video(config.video_url, width=672, height=378)

        style.display_intro_banner()

        style.display_important_message()



    ### GOOGLE CREDENTIALS ###
    credentials_path = google_services.download_service_account_json(st.secrets["jsonkey_google"])
    if credentials_path:
        workbook = google_services.setup_google_drive(credentials_path,"BDD clients opération commerciale")

    ### FORM ###
    form_handling.process_form_submission(credentials = credentials_path, workbook = workbook)

    ### Chatbot ###

    with st.container():
        # Set the style : Banner and hero
        chatbot.set_chatbot_style()
        # Initialize the chatbot
        qa, vectorstore = chatbot.initialize_chatbot(openaikey = st.secrets["openaikey"], pineconekey = st.secrets["pineconekey"], index_name = "agecap")

        # Handle chat interactions
        chatbot.handle_chat_interaction(qa, vectorstore, config.context, config.bot_avatar, config.user_avatar, workbook)

if __name__ == "__main__":
    main()
