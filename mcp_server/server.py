from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

mcp_app = FastAPI(title="MCP Medical Tools")

class SymptomRequest(BaseModel):
    symptoms: str

@mcp_app.post("/tools/recommend_care")
def recommend_care(req: SymptomRequest):
    """Outil MCP qui retourne une recommandation basée sur les symptômes."""
    text = req.symptoms.lower()
    if "douleur thoracique" in text:
        rec = "URGENCE : Consultez immédiatement ou appelez le 15."
    elif "fièvre" in text and "difficulté respiratoire" in text:
        rec = "Risque d'infection respiratoire sévère. Consultez rapidement votre médecin."
    elif "asthme" in text:
        rec = "Utiliser votre bronchodilatateur. Si aggravation, allez aux urgences."
    else:
        rec = "Repos, hydratation, surveillance. Consultez si les symptômes persistent ou s'aggravent."
    return {"recommendation": rec}

if __name__ == "__main__":
    uvicorn.run(mcp_app, host="0.0.0.0", port=8001)