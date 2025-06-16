
import streamlit as st
import time
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os

# Liste noire de mots techniques à filtrer
mots_interdits = [
    "pandas", "docx", "pdfminer", "openpyxl", "imaplib", "smtplib",
    "requests", "BeautifulSoup", "sqlite3", "LangChain", "Ollama", "Mistral",
    "scikit-learn", "transformers", "spaCy",
    "OCR", "NLP", "scraping", "API", "token", "authentification", "JSON",
    "embedding", "LLM", "fine-tuning", "parsing", "workflow", "pipeline"
]

# CSS pour masquer la barre supérieure
st.markdown("""
    <style>
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Générateur d'agents IA")

st.markdown("""
Décrivez clairement le processus, la tâche ou la pratique managériale que vous souhaitez automatiser ou optimiser grâce à un agent IA. 
Ce générateur vous fournit une architecture fonctionnelle claire et rigoureuse, qui vous permet de comprendre précisément le fonctionnement de votre agent IA. 
Elle repose sur les quatre piliers de la méthode ARTS : Accès, Récupération, Traitement et Synthèse. 
À partir de cette architecture fonctionnelle, nous pourrons construire l’architecture technologique correspondante, en identifiant et en déployant les outils les plus adaptés pour créer des agents IA locaux, sur mesure et performants, tout en maintenant des coûts d’utilisation très faibles.
""")
# Initialisation du champ de saisie dans session_state
if "description" not in st.session_state:
    st.session_state.description = ""

if "reponse" not in st.session_state:
    st.session_state.reponse = ""

if "verrouiller" not in st.session_state:
    st.session_state.verrouiller = False

# Fonction de réinitialisation
def reset_app():
    st.session_state.clear()
    st.rerun()

# Champ de saisie libre lié au session_state
st.session_state.description = st.text_area("📝 Décrivez ici l'agent souhaité", value=st.session_state.description, height=200)

# Affichage du bouton uniquement si non verrouillé
if not st.session_state.verrouiller:
    if st.button("🎯 Générer l'architecture fonctionnelle"):
        if st.session_state.description.strip() == "":
            st.warning("Merci de décrire d'abord l’agent que vous souhaitez.")
        else:
            st.session_state.verrouiller = True
            st.rerun()

# Si verrou activé mais réponse non encore générée → lancer la génération
if st.session_state.verrouiller and not st.session_state.reponse:
    start_time = time.time()
    with st.spinner("⏳ L’architecture fonctionnelle est en cours d'élaboration. Temps estimé : environ 2 minutes."):
        template = PromptTemplate.from_template("""
Tu es un assistant en automatisation des processus client. À partir de la description suivante, propose un plan clair structuré selon la méthode ARTS :

- Accès : où l’agent va chercher l’information (en termes simples)
- Récupération : quelles informations l'agent extrait ou détecte
- Traitement : ce que l’agent fait avec ces informations (analyse, tri, sélection...)
- Synthèse : ce que l’agent produit ou restitue (tableau, résumé, alerte...)

Contraintes stylistiques :
- Adopte un langage qui évoque les technologies avancées d’intelligence artificielle sans jamais être technique.
- Tu peux employer des expressions générales et suggestives liées à l’IA générative, aux agents intelligents, à la restitution en langage naturel ou à l’analyse contextuelle.
- Inspire confiance par la clarté et par une formulation professionnelle, en évitant les détails sur les technologies, bibliothèques, langages de programmation ou outils utilisés.
- Tu ne dois jamais répéter de manière mécanique une formule donnée : varie les tournures, adapte-les au contexte, reste fluide et naturel dans ta rédaction.
- Utilise une grammaire française soignée. Le mot "agent" est masculin.
- Rédige dans un français correct, sans erreurs de genre.
- Adopte un ton professionnel et neutre. N’utilise pas de formules amicales, familières ou personnalisantes comme “mon ami”, “voici comment nous allons”, “je vous propose”, etc.

Voici la demande du client :
"""
        + st.session_state.description +
        """
Propose le plan ARTS clair et lisible.
""")

        llm = OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])
        chain = template | llm
        st.session_state.reponse = chain.invoke({"description": st.session_state.description})
        elapsed = int(time.time() - start_time)
        st.info(f"✅ Architecture générée en {elapsed} secondes.")

# Affichage du plan généré et du bouton de réinitialisation
if st.session_state.reponse:
    st.markdown("### 🧱 Plan ARTS généré")
    st.markdown(st.session_state.reponse)
    if st.button("🔁 Créer un nouvel agent IA"):
        reset_app()
