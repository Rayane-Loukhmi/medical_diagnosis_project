from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from ..state import MedicalState

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def report_agent_node(state: MedicalState) -> dict:
    """Génère le rapport final structuré."""
    # Assemblage des informations
    initial_info = state.get("patient_initial_info", "")
    qa_pairs = "\n".join([f"Q: {q}\nR: {r}" for q, r in zip(state.get("questions_asked", []), state.get("patient_answers", []))])
    diag_summary = state.get("diagnostic_summary", "")
    interim_care = state.get("interim_care", "")
    physician_treatment = state.get("physician_treatment", "")
    
    prompt = f"""
    Générez un rapport médical final structuré à partir des éléments suivants :
    
    INFORMATIONS INITIALES : {initial_info}
    
    ÉCHANGE PATIENT :
    {qa_pairs}
    
    SYNTHÈSE CLINIQUE PRÉLIMINAIRE : {diag_summary}
    RECOMMANDATION INTERMÉDIAIRE : {interim_care}
    AVIS MÉDECIN (traitement/conduite) : {physician_treatment}
    
    Le rapport doit contenir les sections :
    1. Motif de la consultation
    2. Analyse des symptômes
    3. Synthèse clinique préliminaire
    4. Recommandations (incluant l'avis médecin)
    5. Mention obligatoire : "Ce système ne remplace pas une consultation médicale."
    
    Format professionnel, en français.
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    final_report = response.content
    
    return {"final_report": final_report, "next": "supervisor"}