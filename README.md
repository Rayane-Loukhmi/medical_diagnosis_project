# Projet Multi-Agents Médical - Orientation Clinique

## Architecture
- **Backend** : FastAPI + LangGraph (Supervisor, DiagnosticAgent, PhysicianReview, ReportAgent)
- **MCP** : Serveur d'outils médicaux (recommandations)
- **Frontend** : Streamlit

## Installation et exécution (sans Docker)

1. Créer un environnement Python 3.10+
2. Installer les dépendances :
```bash
cd backend
pip install -r requirements.txt
cd ../mcp_server
pip install fastapi uvicorn
cd ../frontend
pip install -r requirements.txt