import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pdfkit
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

    # Convert HTML content to PDF
    output_pdf_path = 'devis.pdf'
    pdfkit.from_string(devis_html_content, output_pdf_path)

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

    # Attach the PDF file
    with open(output_pdf_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={output_pdf_path}')
        msg.attach(part)

    # Send the email
    server.sendmail(email, destinataire, msg.as_string())

    # Close the connection
    server.quit()
