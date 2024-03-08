import base64
import streamlit as st
from utils import config

def set_text_color():
    # Set label, radio options, and error message text color to black, including a broader targeting for radio options
    text_color_css = """
    <style>
    /* Target labels of input elements */
    .stTextInput label, .stSelectbox label, .stDateInput label, .stTimeInput label, .stCheckbox label,
    .stRadio label, .stFileUploader label, .stSlider label, .stNumberInput label {
        color: #000; /* Black color for labels */
    }
    /* Broader targeting for radio button options */
    .stRadio > div, .stRadio > div > label {
        color: #000 !important; /* Force black color for radio options */
    }
    /* Target text in Streamlit error messages */
    .stAlert[data-baseweb="notification"] {
        color: #000; /* Black color for error text */
    }
    </style>
    """
    st.markdown(text_color_css, unsafe_allow_html=True)


# Call set_text_color() in your main app function to apply the styles

def set_label_text_color():
    # Set label text color to black
    label_text_color_css = """
    <style>
    /* Target the labels of input elements */
    .stTextInput label, .stSelectbox label, .stDateInput label, .stTimeInput label, .stCheckbox label,
    .stRadio label, .stFileUploader label, .stSlider label {
        color: #000; /* Black color */
    }
    </style>
    """
    st.markdown(label_text_color_css, unsafe_allow_html=True)

def set_app_layout(doodle_path):
    # Set background image
    set_bg_image(doodle_path, deploy=True)


    # Hide Streamlit's menu and footer
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """

    # Hide 'press enter to submit form'
    st.markdown("""
        <style>
            .stTextInput>div>div>span {
                display: none;
            }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    css = """
    <style>
        [data-testid="stForm"] {
            background:  #FFFFFF;
        }
    </style>
    """
    st.write(css, unsafe_allow_html=True)

    return

def embed_youtube_video(url, width=560, height=315):
    # Extract the YouTube video ID from the URL
    video_id = url.split("v=")[1]
    # Define custom HTML for embedding the video within a styled container
    video_html = f"""
        <div style="margin: 10px auto; width: {width}px; border-radius: 20px; overflow: hidden; box-shadow: 0 0 20px rgba(0,0,0,0.1);">
            <iframe width="{width}" height="{height}" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
    """
    # Use st.markdown to render the custom video container
    st.markdown(video_html, unsafe_allow_html=True)

def embed_vimeo_video(url, width=560, height=315):
    # Extract the Vimeo video ID from the URL
    video_id = url.split("/")[-1].split("?")[0]
    # Define custom HTML for embedding the video within a styled container
    video_html = f"""
        <style>
            .video-container {{
                position: relative;
                width: 100%;
                padding-bottom: 56.25%; /* Aspect Ratio 16:9 */
                margin: 10px auto;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
            }}
            .video-iframe {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
            }}
        </style>
        <div class="video-container">
            <iframe class="video-iframe" src="https://player.vimeo.com/video/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
    """
    # Use st.markdown to render the custom video container
    st.markdown(video_html, unsafe_allow_html=True)


def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded_string}"


def set_bg_image(image_path, opacity=0.9, deploy=True):  # Increase opacity for better visibility
    if not deploy:
        base64_image = get_image_base64(image_path)
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, {opacity}), rgba(255, 255, 255, {opacity})), url("data:image/png;base64,{base64_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, {opacity}), rgba(255, 255, 255, {opacity})), url("{image_path}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """, unsafe_allow_html=True)

def display_intro_banner():
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

    return

def banner_questionnaire_medical():
    st.markdown("""
                <style>
                    .banner {
                        display: inline-block;
                        color: #fff;  /* Couleur du texte blanc */
                        padding: 10px 20px;  /* Espacement à l'intérieur de la bannière */
                        border-radius: 10px;  /* Coins arrondis pour un look plus doux */
                        background: linear-gradient(120deg, #6CB2E4 0%, #012B5C 100%);  /* Arrière-plan en dégradé */
                        box-shadow: 0 4px 6px 0 rgba(0,0,0,0.2);  /* Ombre subtile pour la profondeur */
                        margin-top: 20px;  /* Marge en haut */
                        text-align: center;  /* Centrer le texte */
                        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;  /* Police moderne et lisible */
                        font-size: 24px;  /* Taille de police légèrement plus grande pour l'impact */
                        font-weight: bold;  /* Poids de police en gras pour un impact maximal */
                    }
                    .banner-container {
                        text-align: center;  /* Centre la bannière dans le conteneur */
                    }
                </style>
                <div class="banner-container">
                    <div class="banner">
                        Questionnaire Médical
                    </div>
                </div>
                """, unsafe_allow_html=True)

def display_important_message():
    st.markdown("""
        <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-top: 10px; margin-bottom: 10px; color: #000; font-size: 14px;">
            <strong>Note importante :</strong> La tarification de votre devis est précisément ajustée en fonction de la <strong>date de naissance</strong> de chaque membre de la famille. Il est donc essentiel de remplir ces champs avec exactitude pour assurer une estimation adéquate de votre devis.
        </div>
    """, unsafe_allow_html=True)

def display_chat_indication_message():
    st.markdown("""
        <div style="background-color: #e6ffe6; padding: 10px; border-radius: 5px; margin-top: 3px; margin-bottom: 10px; color: #006400; font-size: 14px;">
            <strong>Chattez avec nous en direct :</strong> Sur mobile, appuyez sur la petite flèche "<strong>></strong>" en haut à gauche de votre écran pour poser vos questions. 
        </div>
    """, unsafe_allow_html=True)


def create_columns():
    # Create columns in the Streamlit app
    col1, col2, col3 = st.columns([1,2,1])
    return col1, col2, col3

def place_logo(col2,logo):
    # Function to place the logo image in the specified column
    with col2:
        st.image(logo)


def set_language(lang):
    st.session_state.language = lang

def initialize_language_selection():
    # Define a function to set the language in session state
    # Initialize session state for language if it's not already set
    if 'language' not in st.session_state:
        st.session_state.language = "french"  # Default language

    # Language selection buttons
    if st.button('Français', type = "primary"):
        set_language("fr")
    if st.button('العربية', type = "primary"):
        set_language("ar")


