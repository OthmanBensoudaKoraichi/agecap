import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

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
    msg['Subject'] = "Sujet de l'email"

    # Corps de l'email
    body = "Cher client,Merci d'avoir entamé le processus d'assurance maladie avec nous ! Votre démarche proactive montre votre engagement envers votre santé et celle de votre famille. Pour continuer la démarche, veuillez remplir notre questionnaire en ligne. Contactez-nous par téléphone au 05 22 22 41 80 ou sur l'adresse email assistance.agecap@gmail.com pour toute question. "

    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()

    # Envoyer l'email
    server.sendmail(email, destinataire, text)

    # Fermer la connexion
    server.quit()