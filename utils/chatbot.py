import streamlit as st
from utils import google_services,config
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Pinecone as lpn
from pinecone import Pinecone as pn

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
    with st.container():
        with st.expander(label = "Ouvrir/Fermer le chat", expanded = True):
            with st.container(height = 300,border = True) :
                # Iterate over the chat history in reverse order
                for message in st.session_state.messages:
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
                    font-size: 24px;  /* Slightly larger font size for impact */
                    font-weight: bold;  /* Medium font weight */
                }
                .speech-bubble {
                    position: relative;
                    background: #6CB2E4;
                    border-radius: .4em;
                    color: #fff;
                    padding: 20px;
                    text-align: center;
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                    font-size: 18px;
                    font-weight: 500;
                    margin-bottom: 20px;
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
            </style>
            <div class="chat-banner">Chattez avec nous !</div>
            """, unsafe_allow_html=True)

        colbot1, colbot2 = st.columns([1, 3], gap='small')

        with colbot1:
            st.image(config.hero_path, width=150)

        with colbot2:
            st.markdown("""
                <div class="speech-bubble">
                    Posez une question sur notre assurance maladie complémentaire et recevez une réponse instantanément.
                </div>
            """, unsafe_allow_html=True)

