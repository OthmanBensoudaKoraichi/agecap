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
        with st.container(height = 500, border = True) :
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
            # Append user query to chat history
            st.session_state.messages.append({"role": "Vous", "content": query})

            # Get response from the chatbot
            response = get_chatbot_response(qa, vectorstore, context, query)

            # Append chatbot response to chat history
            st.session_state.messages.append({"role": "Assistant Agecap", "content": response})

            # Format the current interaction
            current_interaction = f"Client: {query} ----- Assistant Agecap: {response}"

            # Display chat history
            display_chat_history(user_avatar, bot_avatar)

            # Append chat history to the Google Sheet
            google_services.append_data_to_sheet("chat", workbook.sheet1, num_devis=st.session_state.id_devis, data=current_interaction)



def set_chatbot_style():
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
            <div class="chat-banner">Chattez avec nous !</div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div class="flex-container">
                <img src="{hero_path}" width="100" />
                <div class="speech-bubble">
                    Posez une question sur notre assurance maladie complémentaire et recevez une réponse instantanément.
                </div>
            </div>
        """.format(hero_path=config.hero_path), unsafe_allow_html=True)


def display_chat_buttons(workbook) :
    float_init()
    # Container with expand/collapse button
    button_chat = st.container()
    with button_chat:
        if st.button('Chatter 👨🏻‍💻', on_click=st.session_state.handler.extend,
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
    with st.sidebar:
        # Set the style : Banner and hero
        set_chatbot_style()
        # Initialize the chatbot
        qa, vectorstore = initialize_chatbot(openaikey=st.secrets["openaikey"],
                                                     pineconekey=st.secrets["pineconekey"], index_name="agecap")

        # Handle chat interactions
        handle_chat_interaction(qa, vectorstore, config.context, config.bot_avatar, config.user_avatar,
                                        workbook)