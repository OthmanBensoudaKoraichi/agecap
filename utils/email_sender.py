import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

def send_email(destinataire, temp_file_path):
    # Contenu HTML supplémentaire à ajouter au début ou à la fin du devis
    additional_html_content = f"""
    <html>
        <body>
            <h1>Cher client,</h1>
            <p>Merci d'avoir entamé le processus d'assurance maladie avec nous ! Votre démarche proactive montre votre engagement envers votre santé et celle de votre famille.</p>
            <p>Pour continuer la démarche, veuillez remplir notre questionnaire en ligne en entrant votre numéro de devis : <strong>{st.session_state.id_devis}</strong></p>
            <p>Le lien du questionnaire est le suivant : <a href="https://agecap.streamlit.app/Questionnaire_Médical">Remplir le questionnaire</a>.</p>
            <p>Contactez-nous par téléphone au 05 22 22 41 80 ou sur l'adresse email assistance.agecap@gmail.com pour toute question.</p>
            <p>Cordialement,<br>L'équipe Agecap.</p>
        </body>
    </html>
    """

    # Lire le contenu HTML du devis à partir du fichier temporaire
    with open(temp_file_path, 'r') as file:
        devis_html_content = file.read()

    # Combine the additional content with the quote content
    combined_html_content = additional_html_content + devis_html_content  # Example: Adding before the quote

    email_subject = f"Devis Assurance Maladie Complémentaire n° {st.session_state.id_devis}"

    # Connection information
    email = st.secrets["email"]
    password = st.secrets["mdp"]

    # Create a secure connection with the SMTP server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email, password)

    # Create the multipart email
    msg = MIMEMultipart('alternative')
    msg['From'] = email
    msg['To'] = destinataire
    msg['Subject'] = email_subject

    # Insert the combined content into the email body
    msg.attach(MIMEText(combined_html_content, 'html'))

    # Send the email
    server.sendmail(email, destinataire, msg.as_string())

    # Close the connection
    server.quit()
