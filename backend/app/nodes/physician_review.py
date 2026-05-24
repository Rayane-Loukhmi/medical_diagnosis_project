from langgraph.types import interrupt, Command
from ..state import MedicalState

def physician_review_node(state: MedicalState) -> Command | dict:
    """
    Nœud avec Human-in-the-Loop. Interrompt l'exécution pour que le médecin
    saisisse son avis (traitement / conduite à tenir).
    """
    # Récupérer la synthèse et la recommandation intermédiaire
    diag_summary = state.get("diagnostic_summary", "Non disponible")
    interim = state.get("interim_care", "Non disponible")
    
    # Présenter au médecin via l'interruption
    physician_input = interrupt({
        "type": "physician_review",
        "message": f"Synthèse clinique préliminaire : {diag_summary}\nRecommandation intermédiaire : {interim}\nVeuillez entrer votre traitement ou conduite à tenir :",
        "prompt": "Traitement ou conduite à tenir :"
    })
    
    # Le médecin doit fournir une chaîne (dans l'interface, on capture via un champ)
    treatment = physician_input if isinstance(physician_input, str) else physician_input.get("treatment", "")
    
    # Mise à jour de l'état et passage au superviseur
    return Command(goto="supervisor", update={"physician_treatment": treatment})