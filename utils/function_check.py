import re
import streamlit as st


# Function to validate Moroccan number
def is_valid_number(number):
    return re.match(r"0+[5-9]\d{8}$", number)


# Function to validate email
def is_valid_email(email):
    return re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email)


# Function to increment family count
def increment_family_count():
    if "family_count" in st.session_state:
        if st.session_state["family_count"] < 7:  # 7 because the index starts at 0
            st.session_state["family_count"] += 1
        else:
            st.warning("Le maximum de 7 membres a été atteint.")
