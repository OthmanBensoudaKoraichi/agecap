import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st

def send_email(destinataire, attachment_filepath=None):
    email_body = """
    Cher client,

    Merci d'avoir entamé le processus d'assurance maladie avec nous ! Votre démarche proactive montre votre engagement envers votre santé et celle de votre famille.

    Pour continuer la démarche, veuillez remplir notre questionnaire en ligne en entrant votre numéro de devis : {num_devis}

    Contactez-nous par téléphone au 05 22 22 41 80 ou sur l'adresse email assistance.agecap@gmail.com pour toute question.

    Cordialement,
    L'équipe Agecap.
    """.format(num_devis=st.session_state.id_devis)

    email_subject = "Devis assurance maladie complémentaire"

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
    msg['Subject'] = email_subject

    # Corps de l'email
    body = email_body
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
            f'attachment; filename= {"Devis " + st.session_state.id_devis}',
        )
        msg.attach(part)

    text = msg.as_string()

    # Envoyer l'email
    server.sendmail(email, destinataire, text)

    # Fermer la connexion
    server.quit()
