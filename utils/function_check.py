import re
import streamlit as st

# Function to validate Moroccan number
def is_valid_number(number):
    return re.match(r'0+[5-9]\d{8}$', number)

# Function to validate email
def is_valid_email(email):
    return re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)

# Function to increment family count
def increment_family_count():
    if st.session_state.family_count < 7:
        st.session_state.family_count += 1
    else:
        pass