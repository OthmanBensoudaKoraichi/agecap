import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st
from utils import config

def send_email(destinataire, attachment_filepath=None):
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

    # Attacher le fichier, si attachment_filepath est fourni
    if attachment_filepath:
        # Ouvrir le fichier en mode binaire
        with open(attachment_filepath, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        # Encoder le fichier en base64 pour l'envoi par email
        encoders.encode_base64(part)
        # Ajouter un en-tête pour que l'email sache ce qu'il y a dans l'attachement
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {"Devis ".join(st.session_state.id_devis)}',
        )
        msg.attach(part)

    text = msg.as_string()

    # Envoyer l'email
    server.sendmail(email, destinataire, text)

    # Fermer la connexion
    server.quit()
