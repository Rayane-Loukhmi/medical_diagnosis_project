from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")   

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
from .graph import build_graph

app = FastAPI(title="Medical Multi-Agent API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

graph = build_graph()

class StartSessionRequest(BaseModel):
    initial_info: str

class ResumeRequest(BaseModel):
    thread_id: str
    user_response: Any

# Stockage simple pour suivre les threads
threads = {}

@app.post("/sessions/start")
async def start_session(req: StartSessionRequest):
    thread_id = str(uuid.uuid4())
    initial_state = {
        "patient_initial_info": req.initial_info,
        "question_count": 0,
        "questions_asked": [],
        "patient_answers": [],
        "next": "diagnostic_agent"
    }
    config = {"configurable": {"thread_id": thread_id}}
    # On lance le graphe jusqu'à la première interruption
    try:
        # Utiliser invoke avec stream_mode="values" pour obtenir l'état
        for event in graph.stream(initial_state, config, stream_mode="values"):
            # On enregistre le dernier état
            threads[thread_id] = event
            # Si interruption, on sort
            if "__interrupt__" in event:
                break
    except Exception as e:
        # L'interruption lève une exception, on l'ignore
        pass
    return {"thread_id": thread_id}

@app.get("/consultation/{thread_id}")
async def get_consultation(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    state = graph.get_state(config)
    if not state:
        raise HTTPException(404, "Thread not found")
    # Récupérer la première interruption en cours
    interrupt = None
    if state.tasks and state.tasks[0].interrupts:
        interrupt = state.tasks[0].interrupts[0].value
    return {
        "state": state.values,
        "interrupt": interrupt
    }

@app.post("/consultation/resume")
async def resume_consultation(req: ResumeRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    # Reprendre avec la réponse
    try:
        for event in graph.stream(Command(resume=req.user_response), config, stream_mode="values"):
            # Stocker le dernier état
            threads[req.thread_id] = event
            if "__interrupt__" in event:
                break
    except Exception:
        pass
    return {"status": "resumed"}

@app.get("/consultation/{thread_id}/report")
async def get_report(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    state = graph.get_state(config)
    if not state or not state.values:
        raise HTTPException(404, "No state found")
    report = state.values.get("final_report", "Rapport non encore généré.")
    return {"report": report}