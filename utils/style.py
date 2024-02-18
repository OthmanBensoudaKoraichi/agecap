import base64
import streamlit as st
from utils import config


def set_app_layout(doodle_path):
    # Set background image
    set_bg_image(doodle_path, deploy=True)

    # Define and inject custom CSS
    custom_css = """
    <style>
    div[data-testid="stSidebar"] > div:first-child {
        background-color: rgba(255,255,255,0.5);
    }
    div[data-testid="stHeader"] {
        background-color: rgba(255,255,255,0.8);
    }
    div[data-testid="stBody"] {
        background-color: rgba(255,255,255,0.8);
    }
    /* Add more custom CSS if needed */
    </style>
    """

    # Inject the custom CSS into the Streamlit app
    st.markdown(custom_css, unsafe_allow_html=True)

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
        <div style="margin: 10px auto; width: {width}px; border-radius: 20px; overflow: hidden; box-shadow: 0 0 20px rgba(0,0,0,0.1);">
            <iframe width="{width}" height="{height}" src="https://player.vimeo.com/video/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
    """
    # Use st.markdown to render the custom video container
    st.markdown(video_html, unsafe_allow_html=True)


def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded_string}"


def set_bg_image(image_path, opacity=0.8, deploy=True):
    # Assuming opacity is between 0 (fully transparent) and 1 (fully opaque)
    if not deploy:
        # Function to convert image to Base64 should be defined somewhere
        base64_image = get_image_base64(image_path)

        # Use local CSS to set the background image with the Base64 string and add a transparent overlay using RGBA
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
        # Directly use the image URL and ensure it's correctly formatted within the url() function
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

        return

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

def display_important_message():
    # Ajout d'une note sous la bannière
    st.markdown("""
        <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-top: 10px; margin-bottom: 10px;">
            <strong>Note importante :</strong> La tarification de votre devis est précisément ajustée en fonction de la <strong>date de naissance</strong> de chaque membre de la famille. Il est donc essentiel de remplir ces champs avec exactitude pour assurer une estimation adéquate de votre devis.
        </div>
    """, unsafe_allow_html=True)

    return

def create_columns():
    # Create columns in the Streamlit app
    col1, col2, col3 = st.columns([1,2,1])
    return col1, col2, col3

def place_logo(col2,logo):
    # Function to place the logo image in the specified column
    with col2:
        st.image(logo)