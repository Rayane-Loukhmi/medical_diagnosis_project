from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import MedicalState
from .nodes.supervisor import supervisor_node
from .nodes.diagnostic_agent import diagnostic_agent_node
from .nodes.physician_review import physician_review_node
from .nodes.report_agent import report_agent_node

def build_graph():
    workflow = StateGraph(MedicalState)
    
    # Ajout des nœuds
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("diagnostic_agent", diagnostic_agent_node)
    workflow.add_node("physician_review", physician_review_node)
    workflow.add_node("report_agent", report_agent_node)
    
    # Définition des edges
    workflow.set_entry_point("supervisor")
    workflow.add_edge("supervisor", "diagnostic_agent")
    workflow.add_edge("diagnostic_agent", "supervisor")
    workflow.add_edge("supervisor", "physician_review")
    workflow.add_edge("physician_review", "supervisor")
    workflow.add_edge("supervisor", "report_agent")
    workflow.add_edge("report_agent", "supervisor")
    # La condition d'arrêt est gérée dans supervisor (retour END)
    
    # Checkpointer pour gérer les interruptions et la mémoire
    memory = MemorySaver()
    graph = workflow.compile(checkpointer=memory)
    return graph