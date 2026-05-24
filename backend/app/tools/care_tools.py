from langchain_core.tools import tool
from ..state import MedicalState

@tool
def recommend_interim_care(symptoms_summary: str) -> str:
    """Génère une recommandation de soins intermédiaires basée sur la synthèse."""
    # Version simple sans LLM pour l'exemple
    recommendations = {
        "fièvre": "Repos, hydratation, paracétamol si nécessaire, consulter si persistance >3 jours.",
        "toux": "Hydratation, miel, surveillance respiratoire.",
        "douleur thoracique": "CONSULTATION IMMÉDIATE - Ne pas attendre.",
        "asthme": "Respecter traitement habituel, consulter si aggravation."
    }
    for keyword, rec in recommendations.items():
        if keyword.lower() in symptoms_summary.lower():
            return rec
    return "Repos, hydratation, surveillance des symptômes. Consulter si aggravation."