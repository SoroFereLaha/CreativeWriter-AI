import os
import json
import streamlit
# import openai
from openai import OpenAI

# configuration de l'api
CHEMIN_PROJET = os.path.dirname(os.path.abspath(__file__))
configuration = json.load(open(f"{CHEMIN_PROJET}/config.json"))
OPENAI_API_KEY = configuration["OPENAI_API_KEY"]

# Créer le client avec la clé
client = OpenAI(api_key=OPENAI_API_KEY)

# configuration de streamlit
streamlit.set_page_config(
    page_title = " ChatBot d'assistance à l'ecriture ",
    page_icon = "💬",
    layout = "wide"
             "" # centrer le contenu de la page
)

# initialisation d'un chat dans streamlit
# on cree une boucle infinie pour le chat
if "chat_message" not in streamlit.session_state:
    streamlit.session_state.chat_message = []

# tire de page
streamlit.title("✍🏽 ChatBot d'assistance à l'ecriture")

# affichage des conversation precedentes
for message in streamlit.session_state.chat_message:
    with streamlit.chat_message(message["role"]):
        streamlit.markdown(message["content"], unsafe_allow_html=True)

# champ de saisi utilisateur

message_utilisateur = streamlit.chat_input("Poser une question au Bot...")

if message_utilisateur :
    # ajouter et affiche le message de l'utilisateur
    streamlit.chat_message("user").markdown(message_utilisateur)
    streamlit.session_state.chat_message.append({"role" : "user", "content" : message_utilisateur})

# envoi du message utilisateur au modele pré-entrainer
chat_message = [{"role": "system", "content": "Tu es un assistant créatif !"}]
chat_message.extend(streamlit.session_state.chat_message)

reponse = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=chat_message
)

# reponse du modele
reponse_model = reponse.choices[0].message.content
# ajout de la reponse au chat
streamlit.session_state.chat_message.append({"role" : "assistant", "content" : reponse_model})

# affichge de la reponse du modele
with streamlit.chat_message("assistant"):
    streamlit.markdown(reponse_model, unsafe_allow_html=True)