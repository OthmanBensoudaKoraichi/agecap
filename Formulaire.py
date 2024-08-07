# Import libraries
import streamlit as st
from utils import style, google_services, config, chatbot, form_handling
from streamlit_float import *
import time
import streamlit.components.v1 as components
from st_clickable_images import clickable_images


# Main function
def main():

    ### STYLE ###


    st.set_page_config(page_icon=config.favicon, layout="centered", initial_sidebar_state="collapsed",
                           menu_items=None)


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

##########
    # Initialize float feature/capability
    #float_init()

    # Create a container for left-aligned content
   # container = st.container()

    # # Align content to the left
    # with container:
    #     clicked = clickable_images(
    #         [
    #             "https://images.unsplash.com/photo-1565130838609-c3a86655db61?w=700",
    #         ],
    #         titles=[f"Image #{i}" for i in range(5)],
    #         div_style={
    #             "display": "flex",
    #             "justify-content": "flex-start",  # Align images to the left
    #             "align-items": "flex-end",  # Align content to the bottom
    #             "flex-wrap": "wrap",
    #             "height": "100vh",  # Full viewport height to push content to the bottom
    #             "position": "relative",
    #         },
    #         img_style={"margin": "5px", "height": "200px"},
    #     )
    #
    #     st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")

   # container.float()



    ##########

    ### GOOGLE CREDENTIALS ###
    credentials_path = google_services.download_service_account_json(st.secrets["jsonkey_google"])
    if credentials_path:
        workbook = google_services.setup_google_drive(credentials_path,"BDD clients opération commerciale")

    ### FORM ###
    form_handling.process_form_submission(credentials = credentials_path, workbook = workbook)

    ### Chatbot ###


    # Set the style : Banner and hero
    #chatbot.set_chatbot_style()
    # Initialize the chatbot
    qa, vectorstore = chatbot.initialize_chatbot(openaikey = st.secrets["openaikey"], pineconekey = st.secrets["pineconekey"], index_name = "agecap")

    # Handle chat interactions
    chatbot.handle_chat_interaction(qa, vectorstore, config.context, config.bot_avatar, config.user_avatar, workbook)

if __name__ == "__main__":
    main()
