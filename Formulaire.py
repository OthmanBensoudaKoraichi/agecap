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

    with st.container(border = True):
        st.write("**Tel** : 05 22 22 41 80")
        st.write("**Email : assistance.agecap@gmail.com**")
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

    # Float feature initialization
    float_init()


    # Container with expand/collapse button
    button_chat = st.container()
    with button_chat:
        if st.button('Chat instantané 👨🏻‍💻', on_click=st.session_state.handler.extend,
                     args=[['collapsed', 'expanded']], type="secondary", key="blue-button"):
            st.session_state.show = True
            st.rerun()

    st.markdown(
        """
        <style>
        div[data-testid="stButton"] > button {
            background-color: #C8E6C9 ;
            color: white;
            border: 2px solid white;
            font-family: Arial, sans-serif;
            font-size: 16px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #C8E6C9;
            transform: scale(1.05);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
            color : white;
            border: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    button_chat_css = float_css_helper(left="0.5rem", bottom="0.5rem", transition=0)

    # Float button container
    button_chat.float(button_chat_css)


    # Container with expand/collapse button
    button_whatsapp = st.container()
    with button_whatsapp:
        try:
            if st.button('Whatsapp 📞'):
                js_code = """
                <script>
                    window.open("https://api.whatsapp.com/send/?phone=212600202155", "_blank").focus();
                </script>
                """
                st.components.v1.html(js_code)
        except Exception as e:
            st.error(f"Une error inattendue est survenue.")



    button_whatsapp_css = float_css_helper(left="10rem", bottom="0.5rem", transition=0)

    # Float button container
    button_whatsapp.float(button_whatsapp_css)



    ### CHATBOT ###
    with st.sidebar :
        # Set the style : Banner and hero
        chatbot.set_chatbot_style()
        # Initialize the chatbot
        qa, vectorstore = chatbot.initialize_chatbot(openaikey=st.secrets["openaikey"],
                                                     pineconekey=st.secrets["pineconekey"], index_name="agecap")

        # Handle chat interactions
        chatbot.handle_chat_interaction(qa, vectorstore, config.context, config.bot_avatar, config.user_avatar,
                                        workbook)



if __name__ == "__main__":
    main()
