# Projet Multi-Agents Médical - Orientation Clinique

## Présentation générale

Ce projet met en place une **application d’aide au diagnostic médical** basée sur une **architecture multi-agents**. L’objectif est de simuler un parcours clinique où plusieurs agents collaborent pour analyser une situation médicale, vérifier la cohérence des informations et produire un rapport final exploitable.

Le système repose sur trois briques principales :

- **Backend** : API FastAPI + orchestration LangGraph
- **MCP** : serveur d’outils médicaux utilisés par les agents
- **Frontend** : interface utilisateur Streamlit

## Ce qui se passe dans le projet

### 1. Le frontend
Le frontend est une interface **Streamlit** qui permet à l’utilisateur de saisir des informations sur un patient (symptômes, historique, etc.) et d’envoyer cette requête au backend.

### 2. Le backend
Le backend expose une API FastAPI et orchestre le workflow de décision via **LangGraph**. Il contient un graphe de contrôle qui fait passer l’information entre les agents suivants :

- **Supervisor** : agent orchestrateur qui décide quel agent doit agir à chaque étape
- **DiagnosticAgent** : analyse les symptômes et propose des pistes diagnostiques
- **PhysicianReview** : relit et critique le diagnostic proposé, en vérifiant la cohérence clinique
- **ReportAgent** : synthétise les informations et produit un rapport final

### 3. Le serveur MCP
Le serveur MCP fournit des **outils médicaux** (ou des capacités externes) que les agents peuvent utiliser lors de l’analyse. Il sert de couche d’intégration pour des fonctions complémentaires.

## Structure du projet

```text
.
├── backend/
│   ├── app/
│   │   ├── api.py
│   │   ├── graph.py
│   │   ├── state.py
│   │   ├── nodes/
│   │   │   ├── diagnostic_agent.py
│   │   │   ├── physician_review.py
│   │   │   ├── report_agent.py
│   │   │   └── supervisor.py
│   │   └── tools/
│   │       ├── care_tools.py
│   │       ├── mcp_client.py
│   │       └── patient_tools.py
│   ├── langgraph.json
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
├── mcp_server/
│   └── server.py
├── docker-compose.yml
└── README.md
```

## Flux de fonctionnement

1. L’utilisateur saisit une requête dans l’interface Streamlit.
2. Le frontend envoie cette requête au backend FastAPI.
3. Le backend démarre l’orchestration LangGraph.
4. Le **Supervisor** choisit l’agent à appeler.
5. Le **DiagnosticAgent** analyse le cas.
6. Le **PhysicianReview** vérifie et corrige si nécessaire.
7. Le **ReportAgent** produit le rapport final.
8. Le résultat est renvoyé au frontend et affiché à l’utilisateur.

## Pré-requis

- Python 3.10 ou supérieur
- `pip`
- Accès Internet pour installer les dépendances

## Installation et exécution

### Option 1 — Exécution locale sans Docker

#### 1. Créer et activer un environnement virtuel

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### 2. Installer les dépendances

```bash
cd backend
pip install -r requirements.txt

cd ../mcp_server
pip install fastapi uvicorn

cd ../frontend
pip install -r requirements.txt
```

#### 3. Lancer le serveur MCP

```bash
cd ../mcp_server
uvicorn server:app --reload
```

#### 4. Lancer le backend

Ouvrir un nouveau terminal :

```bash
cd backend
uvicorn app.api:app --reload
```

#### 5. Lancer le frontend

Ouvrir un autre terminal :

```bash
cd frontend
streamlit run streamlit_app.py
```

### Option 2 — Exécution avec Docker

```bash
docker-compose up --build
```

## Variables d’environnement

Si votre projet utilise des clés API ou des secrets, créez un fichier `.env` à la racine et ajoutez-y les variables nécessaires.

## Développement et mise à jour du dépôt

Pour mettre à jour le dépôt GitHub après une modification :

```bash
git add .
git commit -m "Votre message de commit"
git push
```

## Dépannage

- **Erreur de dépendances** : vérifiez que vous utilisez bien Python 3.10+
- **Port déjà utilisé** : changez le port des commandes `uvicorn` ou `streamlit`
- **Frontend inaccessible** : assurez-vous que le backend et le MCP sont bien démarrés

## Auteur

Ce projet est un prototype de plateforme de diagnostic médical multi-agents conçu pour démontrer une orchestration d’agents et une interface utilisateur simple.
