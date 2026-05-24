import os
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from ..state import MedicalState
from ..tools.patient_tools import ask_patient_question
from ..tools.mcp_client import get_mcp_recommendation

# Initialisation du LLM (peut être remplacé par Ollama ou autre)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Questions prédéfinies pour la démo (sinon générées par LLM)
PREDEFINED_QUESTIONS = [
    "Quels sont vos symptômes principaux et depuis combien de temps ?",
    "Avez-vous de la fièvre ? Si oui, quelle température ?",
    "Ressentez-vous une douleur thoracique ou des difficultés à respirer ?",
    "Avez-vous des antécédents médicaux pertinents (asthme, diabète, hypertension) ?",
    "Avez-vous voyagé récemment ou été en contact avec une personne malade ?"
]

def diagnostic_agent_node(state: MedicalState) -> dict:
    """
    Pose 5 questions au patient via un tool, génère une synthèse clinique
    préliminaire et une recommandation intermédiaire (via MCP).
    """
    q_count = state.get("question_count", 0)
    
    # Phase 1 : poser les questions une par une
    if q_count < 5:
        # Récupérer la dernière question posée ou commencer
        questions_asked = state.get("questions_asked", [])
        if q_count < len(PREDEFINED_QUESTIONS):
            question = PREDEFINED_QUESTIONS[q_count]
        else:
            # Fallback (ne devrait pas arriver)
            question = "Pouvez-vous décrire vos symptômes ?"
        
        # Utiliser le tool ask_patient_question
        answer = ask_patient_question(question, state.get("messages", []))
        # Mise à jour de l'état
        new_questions = questions_asked + [question]
        new_answers = state.get("patient_answers", []) + [answer]
        
        return {
            "question_count": q_count + 1,
            "questions_asked": new_questions,
            "patient_answers": new_answers,
            "messages": [AIMessage(content=f"Question : {question}"), HumanMessage(content=answer)],
            "next": "diagnostic_agent"  # boucle
        }
    
    # Phase 2 : toutes les questions posées -> générer synthèse et recommandation
    # Construire le prompt pour le LLM
    initial_info = state.get("patient_initial_info", "")
    qa_pairs = "\n".join([f"Q: {q}\nR: {r}" for q, r in zip(state.get("questions_asked", []), state.get("patient_answers", []))])
    prompt = f"""Vous êtes un assistant médical pour une orientation clinique préliminaire.
    Informations initiales du patient : {initial_info}
    Historique des questions/réponses :
    {qa_pairs}
    
    Produisez une synthèse clinique préliminaire concise (max 5 lignes) et une recommandation intermédiaire prudente (repos, hydratation, consultation rapide si aggravation).
    Format:
    SYNTHESE: ...
    RECO_INTERIM: ...
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content
    # Extraction basique
    diagnostic_summary = ""
    interim_care = ""
    for line in content.split("\n"):
        if line.startswith("SYNTHESE:"):
            diagnostic_summary = line.replace("SYNTHESE:", "").strip()
        elif line.startswith("RECO_INTERIM:"):
            interim_care = line.replace("RECO_INTERIM:", "").strip()
    
    # Optionnel : améliorer la recommandation via l'outil MCP
    mcp_rec = get_mcp_recommendation(diagnostic_summary)
    if mcp_rec:
        interim_care += f" (recommandation MCP: {mcp_rec})"
    
    return {
        "diagnostic_summary": diagnostic_summary,
        "interim_care": interim_care,
        "next": "supervisor"  # retour au superviseur pour passer à physician_review
    }