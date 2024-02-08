import sys

sys.path.append("/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/")

import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Pinecone as lpn
from pinecone import Pinecone as pn
from streamlit_gsheets import GSheetsConnection
from utils import calculation, function_check, doc_manip
import datetime
from langchain_core.prompts import PromptTemplate


# Put Agecap's Logo at the top of the form
st.image(
    "/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/files/agecaplogo.png"
)

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# Set background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FAFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Initialize LangChain Chatbot and OpenAI Embeddings
OPENAI_API_KEY = st.secrets["openaikey"]
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.0
)
embed = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)

# Pinecone setup
pc = pn(api_key=st.secrets["pineconekey"])
index = pc.Index("agecap")

# Setup for vectorstore
vectorstore = lpn(index, embed, "text")


template = """  Vous êtes un courtier en assurances basé au Maroc, spécialisé dans les assurances maladies.
    Votre expertise en assurance maladie vous permet de donner des conseils avisés et personnalisés à vos clients,
    en vous appuyant sur votre vaste connaissance du domaine.
    Votre communication avec les clients doit être directe, cordiale et compréhensible, sans mentionner explicitement
    vos sources d'information.
    En cas de question dont la réponse dépasse votre champ de connaissances,
    il est crucial d'admettre de manière transparente que vous ne disposez pas de l'information demandée,
    tout en restant serviable et orienté vers la solution.
    Votre objectif est de répondre aux interrogations de manière aussi naturelle et personnelle que possible,
    comme si vous partagiez votre propre expertise sans faire référence à des documents externes.

    ========================================================================
    {context}
    ========================================================================

    Question: {query}

    """


# Initialize RetrievalQA
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={
        "prompt": PromptTemplate(
            template=template,
            input_variables=["context", "query"],
        ),
    },
)


def main():
    # Display YouTube video
    st.video("https://www.youtube.com/watch?v=A5SuXPftKGc")

    # Initialize session state for family members count
    if "family_count" not in st.session_state:
        st.session_state["family_count"] = 1

    # Read table for the quote
    primes = pd.read_excel(
        "/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/files/sehassur_devis.xlsx",
        sheet_name="primes",
    )
    coefficients = pd.read_excel(
        "/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/files/sehassur_devis.xlsx",
        sheet_name="coefficients",
    )

    # Form for family members and communication preference
    with st.form("insurance_form"):
        family_details = []

        # Input fields for family members
        for i in range(st.session_state["family_count"]):
            member_label = ""
            if i == 0:
                member_label = "Souscripteur"
            else:
                member_label = f"Membre de la famille {i +1}"

            with st.expander(f"{member_label}", expanded=True):
                first_name = st.text_input(f"Prénom", key=f"first_name_{i}")
                surname = st.text_input(f"Nom ", key=f"surname_{i}")
                dob = st.date_input(
                    f"Date de naissance",
                    key=f"dob_{i}",
                    min_value=datetime.datetime.now()
                    - datetime.timedelta(days=365.25 * 100),
                    format="DD-MM-YYYY",
                )
                family_details.append((first_name, surname, dob))

            # Display warning if the maximum number of family members is reached
            if i == 6:  # Check if this is the 7th family member (index 6)
                st.warning("Le maximum de 7 membres a été atteint.")

        # Button to add family members within the form
        st.form_submit_button(
            "Ajouter un membre de la famille",
            on_click=function_check.increment_family_count,
        )

        email_address = st.text_input("Adresse email", key="email")
        if email_address and not function_check.is_valid_email(email_address):
            st.error("Format de l'adresse email invalide")

        phone_number = st.text_input("Numéro de téléphone", key="phone").replace(
            " ", ""
        )
        if phone_number and not function_check.is_valid_number(phone_number):
            st.error("Format du numéro invalide")
        # Final submit button
        submit_button = st.form_submit_button("Calculer le devis")

        if submit_button:
            # Extract family members' dates of birth
            family_dobs = [dob for _, _, dob in family_details]

            # Calculate premiums
            family_premiums = calculation.calculate_family_premiums(
                family_dobs, primes, coefficients
            )

            # Sum premiums
            total_family_premiums = pd.DataFrame.from_dict(
                calculation.sum_family_premiums(family_premiums)
            ).T

            # Insert into word doc
            doc_manip.insert_into_word_doc(
                "/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/files/devis_agecap.docx",
                family_details,
                total_family_premiums,
            )

    st.subheader(
        "Posez une question sur notre assurance maladie complémentaire et recevez une réponse instantanément."
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("Écrivez votre question", key="chatbot_input")

    if query:
        # Display user message in chat message container
        st.chat_message("user").markdown(query)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": query})

        with st.spinner("Veuillez patienter quelques secondes"):
            response = doc_manip.invoke(query= query, qa=qa, k=3)

            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
