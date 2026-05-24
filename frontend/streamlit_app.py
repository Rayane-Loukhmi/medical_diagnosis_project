import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Orientation Clinique", layout="wide")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
    st.session_state.waiting = False

st.title("🏥 Système d'orientation clinique préliminaire")
st.caption("Ce système ne remplace pas une consultation médicale.")

# Écran 1
if st.session_state.thread_id is None:
    with st.form("initial"):
        initial_info = st.text_area("Description du motif et des symptômes principaux :", height=150)
        submitted = st.form_submit_button("Démarrer la consultation")
        if submitted and initial_info.strip():
            r = requests.post(f"{API_URL}/sessions/start", json={"initial_info": initial_info})
            if r.status_code == 200:
                st.session_state.thread_id = r.json()["thread_id"]
                st.session_state.waiting = True
                st.rerun()
            else:
                st.error("Erreur de démarrage")

# Écran 2 : questionnaire patient + médecin + rapport
else:
    # Récupération de l'état
    resp = requests.get(f"{API_URL}/consultation/{st.session_state.thread_id}")
    if resp.status_code != 200:
        st.error("Impossible de récupérer l'état")
        st.stop()
    data = resp.json()
    state = data.get("state", {})
    interrupt = data.get("interrupt")

    # Si rapport final déjà présent
    if state.get("final_report"):
        st.header("Rapport final")
        st.markdown(state["final_report"])
        if st.button("Nouvelle consultation"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.stop()

    # Si présence d'une interruption
    if interrupt:
        itype = interrupt.get("type")
        if itype == "patient_question":
            st.header("Questionnaire patient")
            question = interrupt.get("question")
            st.write(f"**Question :** {question}")
            answer = st.text_input("Votre réponse :", key="patient_answer")
            if st.button("Envoyer"):
                resume = requests.post(f"{API_URL}/consultation/resume",
                                        json={"thread_id": st.session_state.thread_id, "user_response": answer})
                if resume.status_code == 200:
                    st.rerun()
                else:
                    st.error("Erreur envoi réponse")
        elif itype == "physician_review":
            st.header("Avis du médecin traitant")
            st.subheader("Synthèse clinique préliminaire")
            st.write(state.get("diagnostic_summary", ""))
            st.subheader("Recommandation intermédiaire")
            st.write(state.get("interim_care", ""))
            treatment = st.text_area("Traitement / conduite à tenir :", key="treatment")
            if st.button("Valider l'avis médecin"):
                resume = requests.post(f"{API_URL}/consultation/resume",
                                        json={"thread_id": st.session_state.thread_id, "user_response": treatment})
                if resume.status_code == 200:
                    st.rerun()
                else:
                    st.error("Erreur validation médecin")
        else:
            st.info("Interruption inconnue, rechargez.")
    else:
        # Pas d'interruption : soit le graphe a fini, soit il est en cours d'exécution sans attente
        # Vérifier si le diagnostic est terminé (question_count=5)
        if state.get("question_count", 0) >= 5 and state.get("diagnostic_summary") and not state.get("physician_treatment"):
            st.info("Le diagnostic est terminé. Le médecin va être sollicité...")
            # Forcer une actualisation pour déclencher l'interruption médecin
            time.sleep(1)
            st.rerun()
        else:
            st.info("Traitement en cours... actualisez si nécessaire.")
            if st.button("Actualiser"):
                st.rerun()