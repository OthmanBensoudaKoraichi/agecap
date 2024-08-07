import re
import streamlit as st


# Function to validate Moroccan number
def is_valid_number(number):
    # Remove non-numeric characters to normalize the input
    sanitized_number = re.sub(r"\D", "", number)  # \D matches any character that is not a digit

    # Match the normalized number with the pattern for both domestic and international Moroccan formats
    # For domestic format: start with 0 followed by a digit from 5 to 9 and then 8 more digits (total 9 digits after 0)
    # For international format: start with 212 followed by a digit from 5 to 9 and then 8 more digits (total 9 digits after 212)
    return re.match(r"^(0[5-9]\d{8}|212[5-9]\d{8})$", sanitized_number)


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



