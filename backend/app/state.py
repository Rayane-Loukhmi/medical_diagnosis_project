from typing import Annotated, List, Literal, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class MedicalState(TypedDict, total=False):
    messages: Annotated[List, add_messages]
    next: Literal["diagnostic_agent", "physician_review", "report_agent", "FINISH"]
    question_count: int
    patient_initial_info: str
    questions_asked: List[str]
    patient_answers: List[str]
    interim_care: str
    diagnostic_summary: str
    physician_treatment: str
    final_report: str