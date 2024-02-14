import streamlit as st
import base64

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

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded_string}"


def set_bg_image(image_path, opacity=0.8, deploy = True):
    # Assuming opacity is between 0 (fully transparent) and 1 (fully opaque)
    if deploy == False:
        base64_image = get_image_base64(image_path)

        # Use local CSS to set the background image with the Base64 string and add a transparent overlay using RGBA
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, {opacity}), rgba(255, 255, 255, {opacity})), url("{base64_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """, unsafe_allow_html=True)

    else:
        # Use local CSS to set the background image with the Base64 string and add a transparent overlay using RGBA
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, {opacity}), rgba(255, 255, 255, {opacity})), {image_path});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """, unsafe_allow_html=True)
