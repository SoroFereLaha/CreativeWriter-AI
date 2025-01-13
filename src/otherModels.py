import os
import streamlit
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Configuration de streamlit
streamlit.set_page_config(
    page_title="ChatBot d'assistance à l'ecriture",
    page_icon="💬",
    layout="wide"
)

# Choix du modèle
MODEL_NAME = "facebook/roberta-base"  # Pour RoBERTa
# MODEL_NAME = "t5-base"  # Pour T5

# Chargement du modèle et du tokenizer
@streamlit.cache_resource  # Cache pour éviter de recharger le modèle à chaque interaction

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    return model, tokenizer

model, tokenizer = load_model()

# Création du pipeline
generator = pipeline(
    "text-generation" if "roberta" in MODEL_NAME else "text2text-generation",
    model=model,
    tokenizer=tokenizer
)

# Initialisation du chat
if "chat_message" not in streamlit.session_state:
    streamlit.session_state.chat_message = []

# Titre de page
streamlit.title("✍🏽 ChatBot d'assistance à l'ecriture")

# Affichage des conversations précédentes
for message in streamlit.session_state.chat_message:
    with streamlit.chat_message(message["role"]):
        streamlit.markdown(message["content"], unsafe_allow_html=True)

# Champ de saisie utilisateur
message_utilisateur = streamlit.chat_input("Poser une question au Bot...")

if message_utilisateur:
    # Ajout et affichage du message de l'utilisateur
    streamlit.chat_message("user").markdown(message_utilisateur)
    streamlit.session_state.chat_message.append({"role": "user", "content": message_utilisateur})

    # Génération de la réponse
    if "roberta" in MODEL_NAME:
        # Pour RoBERTa
        reponse = generator(
            message_utilisateur,
            max_length=100,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id
        )[0]['generated_text']
    else:
        # Pour T5
        reponse = generator(
            message_utilisateur,
            max_length=100,
            num_return_sequences=1
        )[0]['generated_text']

    # Ajout de la réponse au chat
    streamlit.session_state.chat_message.append({"role": "assistant", "content": reponse})

    # Affichage de la réponse
    with streamlit.chat_message("assistant"):
        streamlit.markdown(reponse, unsafe_allow_html=True)