from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

@tool
def ask_patient_question(question: str, conversation_history: list) -> str:
    """
    Tool qui simule l'interaction avec le patient.
    Dans un vrai frontend, cette fonction serait remplacée par une entrée utilisateur.
    Ici, elle attend une réponse via interruption (pour être compatible avec LangGraph).
    """
    from langgraph.types import interrupt
    # On utilise interrupt() pour obtenir la réponse du patient (géré par l'API/frontend)
    answer = interrupt({
        "type": "patient_question",
        "question": question
    })
    # L'interruption retourne la réponse saisie par l'utilisateur
    if isinstance(answer, dict):
        return answer.get("answer", "")
    return str(answer)