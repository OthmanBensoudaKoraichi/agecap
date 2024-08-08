import streamlit as st
from utils import google_services,config
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Pinecone as lpn
from pinecone import Pinecone as pn
from streamlit_float import *

# Initialize chatbot components
def initialize_chatbot(openaikey,pineconekey,index_name):
    llm = ChatOpenAI(
        openai_api_key=openaikey, model_name="gpt-4o-mini", temperature=0.0
    )
    embed = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=openaikey)
    pc = pn(api_key=pineconekey)
    index = pc.Index(index_name)
    vectorstore = lpn(index, embed, "text")

    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
    )

    return qa, vectorstore

def display_chat_history(user_avatar, bot_avatar):
        with st.container(border = True) :
            # Iterate over the chat history in reverse order
            for message in reversed(st.session_state.messages):
                # Determine the alignment and background color based on the message role
                if message["role"] == "Vous":
                    alignment = "left"
                    background_color = "#E1F5FE"  # Light blue background for the user messages
                    avatar = user_avatar
                else:
                    alignment = "right"
                    background_color = "#C8E6C9"  # Light green background for bot messages
                    avatar = bot_avatar

                # Use markdown to style the message box
                message_box = f"""
                <div style="display: flex; align-items: center; justify-content: {alignment}; margin-bottom: 10px;">
                    <div style="margin: 10px; padding: 10px; background-color: {background_color}; border-radius: 10px; max-width: 80%;">
                        <img src="{avatar}" alt="Avatar" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px;">
                        {message["content"]}
                    </div>
                </div>
                """
                st.markdown(message_box, unsafe_allow_html=True)
        return True


def get_chatbot_response(qa, vectorstore, context, query):
    with st.spinner("Veuillez attendre quelques secondes..."):
        # Perform similarity search with the current query
        vectorstore.similarity_search(query, k=6)

        # Enhance the context with recent chat history before appending the current query
        chat_history = " ".join([f"{msg['role']}: {msg['content']}" for msg in
                                 reversed(st.session_state.messages[-4:])])
        enhanced_context = chat_history + "\n" + context + "\n" + query

        # Query the model with the enhanced context
        response = qa.run(enhanced_context)
        return response

def append_chat_to_sheet(downloaded,sheet):
    if downloaded == True:
        chat_history = "--------".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
        google_services.append_data_to_sheet(sheet, [chat_history])
    else:
        chat_history = "--------".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
        google_services.append_data_to_sheet(sheet, [chat_history])


# Chatbot interaction
def handle_chat_interaction(qa, vectorstore, context, bot_avatar, user_avatar, workbook):
    if 'id_devis' not in st.session_state:
        st.session_state.id_devis = None

    if 'message_sent' not in st.session_state:
        st.session_state.message_sent = False

    # Check if chat history exists in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if len(st.session_state.messages) >= 20:
        # Display a message to the user indicating the limit is reached
        st.success("Nous sommes ravis que vous soyez intéressé(e) par notre produit ! Si vous avez plus de questions, n'hésitez pas à nous appeler au 05 22 22 41 80")
    else:
        # Input from user
        query = st.chat_input("Posez votre question", key="chatbot_input")

        if query:
            st.session_state.messages.append({"role": "Vous", "content": query})

            # Get response from the chatbot
            response = get_chatbot_response(qa, vectorstore, context, query)


            # Append chatbot response to chat history
            st.session_state.messages.append({"role": "Assistant Agecap", "content": response})

            # Format the current interaction
            current_interaction = f"Client: {query} ----- Assistant Agecap: {response}"

            # Append chat history to the Google Sheet
            google_services.append_data_to_sheet("chat", workbook.sheet1, num_devis=st.session_state.id_devis, data=current_interaction)


    # Display chat history
    display_chat_history(user_avatar, bot_avatar)



def set_chatbot_style(message_sent):

    # This function now sets the style within the sidebar
    with st.sidebar:
        # Bannière avec gradient, bords arrondis, et ombre pour un look sophistiqué
        st.markdown("""
            <style>
                .chat-banner {
                    color: #fff;  /* White text color */
                    padding: 10px;  /* Padding inside the banner for spacing */
                    border-radius: 10px;  /* Rounded corners for a softer look */
                    background: linear-gradient(120deg, #6CB2E4 0%, #012B5C 100%);  /* Gradient background */
                    margin-bottom: 20px;  /* Margin at the bottom */
                    text-align: center;  /* Center the text */
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;  /* Modern, readable font */
                    font-size: 20px;  /* Smaller font size */
                    font-weight: bold;  /* Medium font weight */
                }
                .speech-bubble {
                    position: relative;
                    background: #6CB2E4;
                    border-radius: .4em;
                    color: #fff;
                    padding: 10px;
                    text-align: center;
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                    font-size: 14px;
                    font-weight: 500;
                    margin-bottom: 10px;
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

                .flex-container {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                }

                /* Responsive Styles */
                @media (max-width: 768px) {
                    .chat-banner {
                        font-size: 18px;  /* Smaller font size for smaller screens */
                        padding: 8px;  /* Less padding for smaller screens */
                    }
                    .speech-bubble {
                        font-size: 12px;  /* Smaller font size for smaller screens */
                        padding: 8px;  /* Less padding for smaller screens */
                    }
                    .flex-container {
                        flex-direction: column;
                    }
                }

                @media (max-width: 480px) {
                    .chat-banner {
                        font-size: 16px;  /* Even smaller font size for very small screens */
                        padding: 5px;  /* Even less padding for very small screens */
                    }
                    .speech-bubble {
                        font-size: 10px;  /* Even smaller font size for very small screens */
                        padding: 5px;  /* Even less padding for very small screens */
                    }
                    .flex-container {
                        flex-direction: column;
                    }
                }
            </style>
            <div class="chat-banner">Chat instantané</div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div class="flex-container">
                <img src="{hero_path}" width="100" />
                <div class="speech-bubble">
                    Posez une question sur notre assurance maladie complémentaire.
                </div>
            </div>
        """.format(hero_path=config.hero_path), unsafe_allow_html=True)


def display_chat_buttons(workbook,message_sent) :
    float_init()
    # Container with expand/collapse button
    button_chat = st.container()
    with button_chat:
        # Add a unique CSS class to the button
        if st.button('👨🏻‍💻 Web chat', on_click=st.session_state.handler.extend,
                     args=[['collapsed', 'expanded']], type="secondary", key="blue-button"):
            st.session_state.show = True
            st.rerun()

        # Add your custom CSS
        st.markdown(
            """
            <style>
            .st-emotion-cache-qomobe.ef3psqc12 {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 6px 12px; /* Adjusted button size */
                font-size: 15px; /* Font size */
                cursor: pointer;
                background-color: #ff5733; 
                color: white; /* Text color */
                border: 2px solid white; /* White border */
                border-radius: 50px; /* Rounded button */
                text-align: center;
                text-decoration: none;
                font-family: Arial, sans-serif;
                margin: 10px 2px;
                transition: transform 0.3s, box-shadow 0.3s, background-color 0.3s;
                position: fixed; /* Adjust position as needed */
                bottom: 0rem; /* Position at the bottom */
                left: 0.5rem; /* Adjust left position */
            }

            .st-emotion-cache-qomobe.ef3psqc12:hover {
                background-color: #ff5733; /* Slightly darker color on hover */
                transform: scale(1.05);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
                color: white;
            }

            .st-emotion-cache-qomobe.ef3psqc12:link, .st-emotion-cache-qomobe.ef3psqc12:visited, .st-emotion-cache-qomobe.ef3psqc12:hover, .st-emotion-cache-qomobe.ef3psqc12:active {
                color: white;
                text-decoration: none;
            }

            .st-emotion-cache-qomobe.ef3psqc12 img {
                width: 20px; /* Image width */
                height: 20px; /* Image height */
                margin-right: 8px; /* Space between image and text */
            }
            </style>
            """,
            unsafe_allow_html=True
        )


    # Float button container
    button_chat.float()

    # Define the style for the WhatsApp button
    button_style = """
    <style>
        .whatsapp-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 6px 12px; /* Taille du bouton ajustée */
            font-size: 15px; /* Taille de la police */
            cursor: pointer;
            background-color: #25D366; /* Couleur de fond similaire au logo WhatsApp */
            color: white; /* Couleur du texte */
            border: 2px solid white; /* Bordure blanche */
            border-radius: 50px; /* Pour rendre le bouton rond */
            text-align: center;
            text-decoration: none;
            font-family: Arial, sans-serif;
            margin: 10px 2px;
            transition: transform 0.3s, box-shadow 0.3s, background-color 0.3s;
            position: fixed;
            left: 8rem;
            bottom: 0rem;
        }

        .whatsapp-button:hover {
            background-color: #1EBE53; /* Couleur légèrement plus foncée au survol */
            transform: scale(1.05);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
            color: white;
        }

        .whatsapp-button:link, .whatsapp-button:visited, .whatsapp-button:hover, .whatsapp-button:active {
            color: white;
            text-decoration: none;
        }

        .whatsapp-button img {
            width: 20px; /* Largeur de l'image */
            height: 20px; /* Hauteur de l'image */
            margin-right: 8px; /* Espace entre l'image et le texte */
        }
    </style>
    """

    # Use st.markdown to render the style
    st.markdown(button_style, unsafe_allow_html=True)

    # Container for the WhatsApp button
    button_whatsapp = st.container()
    with button_whatsapp:
        try:
            # Use a hyperlink to open WhatsApp in a new tab with the defined style
            st.markdown(
                """
                <a href="https://api.whatsapp.com/send/?phone=212761080096" target="_blank" class="whatsapp-button">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp">
                    WhatsApp
                </a>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Une erreur inattendue est survenue : {str(e)}")
    # Float button container
    button_whatsapp.float()

    ### CHATBOT ###
    with st.sidebar:
        # Set the style : Banner and hero
        set_chatbot_style(message_sent=message_sent)
        # Initialize the chatbot
        qa, vectorstore = initialize_chatbot(openaikey=st.secrets["openaikey"],
                                                     pineconekey=st.secrets["pineconekey"], index_name="agecap")

        # Handle chat interactions
        handle_chat_interaction(qa, vectorstore, config.context, config.bot_avatar, config.user_avatar,
                                        workbook)