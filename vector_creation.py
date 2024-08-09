# Import necessary libraries
from pinecone import Pinecone,ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
from langchain_community.document_loaders import PyPDFLoader
from tqdm.auto import tqdm
from uuid import uuid4
import streamlit as st
import time
from openai import OpenAIError


# Initialize tokenizer
tokenizer = tiktoken.get_encoding("cl100k_base")

# Create the length function using tiktoken
def tiktoken_len(text):
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)

# Create a text splitter using RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=tiktoken_len,
    separators=["\n\n", "\n", " ", ""],
)


# Initialize Pinecone
pc = Pinecone(api_key=st.secrets["pineconekey"])

pc.create_index(
    name="sanad",
    dimension=3072, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

# Set the Pinecone index to "agecap"
index = pc.Index("sanad")

# Initialize OpenAI Embeddings
embed = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=st.secrets["openaikey"],
)

# Define paths to your PDF files
pdf_paths = [
    "/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/files/sanad_conditions.pdf",
    "/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/files/sanad_fiche_produit.pdf",
    "/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/files/sanad_notice.pdf",
]

# Function to process a batch of texts and metadatas
def process_batch(texts, metadatas):
    ids = [str(uuid4()) for _ in range(len(texts))]
    embeds = embed.embed_documents(texts)
    index.upsert(vectors=zip(ids, embeds, metadatas))
    return True

# Main processing loop for each PDF file
for pdf_path in pdf_paths:
    # Load and split PDF
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    texts = []
    metadatas = []

    for page_num, page in enumerate(tqdm(pages)):
        # Split text into chunks
        record_texts = text_splitter.split_text(page.page_content)
        record_metadatas = [
            {"page": page_num, "chunk": i, "text": chunk}
            for i, chunk in enumerate(record_texts)
        ]

        texts.extend(record_texts)
        metadatas.extend(record_metadatas)

        if len(texts) >= 100:
            success = process_batch(texts, metadatas)
            if success:
                texts, metadatas = [], []

    # Process remaining texts
    if texts:
        success = process_batch(texts, metadatas)
        if success:
            texts, metadatas = [], []

print("Processing complete.")
