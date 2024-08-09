import streamlit as st

# Setting all variables used in main
agecap_logo = "https://github.com/OthmanBensoudaKoraichi/agecap/blob/master/files/agecaplogo.png?raw=true"
doodle = "https://raw.githubusercontent.com/OthmanBensoudaKoraichi/agecap/master/files/doodle.png"
primes_and_coef = "https://raw.githubusercontent.com/OthmanBensoudaKoraichi/agecap/master/files/sehassur_devis.xlsx"
devis_doc = "https://raw.githubusercontent.com/OthmanBensoudaKoraichi/agecap/master/files/devis_agecap.docx"
hero_path = "https://github.com/OthmanBensoudaKoraichi/agecap/blob/master/files/agecap_hero.png?raw=true"
user_avatar = 'https://github.com/OthmanBensoudaKoraichi/agecap/blob/master/files/user_avatar.png?raw=true'
bot_avatar = 'https://github.com/OthmanBensoudaKoraichi/agecap/blob/master/files/agecaplogosmall.png?raw=true'
video_url = "https://vimeo.com/913774763?share=copy"
favicon = 'https://github.com/OthmanBensoudaKoraichi/agecap/blob/master/files/agecap_favicon.png?raw=true'
folder_id = '1jzqRv_SvUz1EkeV0AnlgY00PaTKhXjm4'
devis_html = {"AXA" : "https://raw.githubusercontent.com/OthmanBensoudaKoraichi/agecap/master/files/devis_agecap.html", "SANAD" : "https://raw.githubusercontent.com/OthmanBensoudaKoraichi/agecap/master/files/devis_sanad.html"}

months = {
    'Janvier': 1,
    'Février': 2,
    'Mars': 3,
    'Avril': 4,
    'Mai': 5,
    'Juin': 6,
    'Juillet': 7,
    'Août': 8,
    'Septembre': 9,
    'Octobre': 10,
    'Novembre': 11,
    'Décembre': 12
}


context = (
    "Vous êtes Agecap, un courtier en assurances basé au Maroc, spécialisé dans les assurances maladies. Vous vendez un produit d'assurance complémentaire (AMC) à l'assurance obligatoire (AMO), et vous répondez aux questions de vos clients dans un chat."
    "Votre expertise en assurance maladie vous permet de donner des conseils avisés et personnalisés à vos clients, "
    "en vous appuyant sur votre vaste connaissance du domaine. Vous proposez des devis instantanés sur votre app : https://agecap.streamlit.app/. "
    "Votre communication avec les clients doit être directe, cordiale et compréhensible, sans mentionner explicitement "
    "vos sources d'information. "
    "En cas de question dont la réponse dépasse votre champ de connaissances, "
    "il est crucial d'admettre de manière transparente que vous ne disposez pas de l'information demandée, "
    "tout en restant serviable et orienté vers la solution. Soyez toujours le plus concis possible. Si vous ne connaissez pas une réponse, donnez le contact d'Agecap. "
    "Votre objectif est de répondre aux interrogations de manière aussi naturelle et personnelle que possible, "
    "comme si vous partagiez votre propre expertise sans faire référence à des documents externes. Si l'utilisateur ne mentionne pas de produit d'assurance spécifique, considérez que ses questions se rapportent au produit d'assurance maladie complémentaire dont vous disposez des informations. "
    "Lorsque l'on vous demande des informations de contact, vous ne donnez que le contact d'Agecap : "
    "Téléphone : 05 22 22 41 80"
    "Adresse : 88 Avenue Mers Sultan, Casablanca"
    "Adresse email : assistance.agecap@gmail.com"
    "Voici la question de l'utilisateur : "
)

language_dict = {
    "fr": {
        "Bannière principale" : "Remplissez notre formulaire et obtenez devis en 1 clic !" ,
        "Prénom": "Prénom",
        "Note importante" : "<strong>Note importante :</strong> La tarification de votre devis est précisément ajustée en fonction de la <strong>date de naissance</strong> de chaque membre de la famille. Il est donc essentiel de remplir ces champs avec exactitude pour assurer une estimation adéquate de votre devis.",
        "Nom de famille": "Nom de famille",
        "Date de naissance" : "Date de naissance",
        "membre famille" : "Ajouter un membre de la famille",
        "email" : "Adresse email du souscripteur",
        "tel" : "Numéro de téléphone du souscripteur",
        "Sur quel réseau social avez-vous vu notre formulaire?" : "Sur quel réseau social avez-vous vu notre formulaire?",
        "Linkedin" : "Linkedin",
        "Facebook" : "Facebook",
        "Instagram" : "Ne souhaite pas préciser",
        "Calculer le devis" : "Calculer le devis",
        "redirection" : "Cela vous redirigera vers votre devis en quelques secondes.",
        "Chat banniere" : "Chattez avec nous ! ",
        "Chat message" : "Posez une question sur notre assurance maladie complémentaire et recevez une réponse instantanément.",
        "Posez votre question" : "Posez votre question",

    },
    "ar": {
        "Relation au souscripteur": "Subscriber relationship",
        "Assurance complémentaire": "Do you have supplementary health insurance with another company?"
    }
}

