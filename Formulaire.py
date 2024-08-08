# Import libraries
import streamlit as st
from utils import style, google_services, config, chatbot, form_handling
from streamlit_float import *
import time
import streamlit.components.v1 as components



# Main function
def main():

    ### STYLE ###
    if 'handler' not in st.session_state:
        st.session_state.handler = ['auto']

    if len(st.session_state.handler) > 0:
        state = st.session_state.handler.pop(0)
        st.set_page_config(page_icon=config.favicon, layout="centered", initial_sidebar_state=state,
                           menu_items=None)
        if len(st.session_state.handler) > 0:
            # A little extra wait time as without it sometimes the backend moves "too fast" for the front
            time.sleep(.1)
            st.rerun()

    style.display_contact()
    # Set the layout of the app
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
        workbook = google_services.setup_google_drive(credentials_path, "BDD clients opération commerciale")

    ### FORM ###
    form_handling.process_form_submission(credentials=credentials_path, workbook=workbook)

    chatbot.display_chat_buttons(workbook = workbook)



if __name__ == "__main__":
    main()
