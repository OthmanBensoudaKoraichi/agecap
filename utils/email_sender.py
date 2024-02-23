import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from utils import config

def send_email(destinataire):
    # Informations de connexion
    email = st.secrets["email"]
    password = st.secrets["mdp"]

    # Créer une connexion sécurisée avec le serveur SMTP
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email, password)

    # Créer l'email
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = destinataire
    msg['Subject'] = config.email_subject

    # Corps de l'email
    body = config.email

    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()

    # Envoyer l'email
    server.sendmail(email, destinataire, text)

    # Fermer la connexion
    server.quit()