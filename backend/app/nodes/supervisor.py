from langgraph.graph import END
from ..state import MedicalState

def supervisor_node(state: MedicalState) -> dict:
    """Orchestre le workflow : décide quel agent exécuter ensuite."""
    current_next = state.get("next", "diagnostic_agent")
    
    # Si déjà à FINISH, on termine
    if current_next == "FINISH":
        return {"next": END}
    
    # Logique simple de transition
    if current_next == "diagnostic_agent":
        return {"next": "diagnostic_agent"}
    elif current_next == "physician_review":
        return {"next": "physician_review"}
    elif current_next == "report_agent":
        return {"next": "report_agent"}
    else:
        return {"next": END}