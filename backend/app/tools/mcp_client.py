import httpx
import json
import os

# Simulation d'un client MCP qui appelle le serveur MCP via HTTP (pour simplifier)
# En réalité MCP utilise stdio ou SSE, mais pour la démo on utilise un endpoint REST.
# Ceci respecte l'esprit d'intégration MCP (un outil externe).
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8001")

def get_mcp_recommendation(symptom_text: str) -> str:
    """Appelle l'outil MCP 'recommend_care' pour obtenir une recommandation."""
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.post(
                f"{MCP_SERVER_URL}/tools/recommend_care",
                json={"symptoms": symptom_text}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("recommendation", "")
    except Exception as e:
        print(f"Erreur MCP: {e}")
    return ""