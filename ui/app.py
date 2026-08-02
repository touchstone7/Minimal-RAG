import requests
import streamlit as st

from styles import load_styles
from components import (
    render_header,
    render_api_status,
    render_knowledge_base,
    render_ingest_button,
    render_question_input,
    render_question_buttons,
    render_answer,
    render_footer,
)


# ============================================================
# Configuration
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Minimal RAG",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# Styling
# ============================================================

load_styles()


# ============================================================
# API Functions
# ============================================================

def check_api():

    try:

        response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=3,
        )

        return response.status_code == 200

    except requests.RequestException:

        return False


def ingest_documents():

    try:

        response = requests.post(
            f"{API_BASE_URL}/ingest",
            timeout=120,
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:

        return {
            "error": str(error)
        }


def ask_question(question):

    try:

        response = requests.post(
            f"{API_BASE_URL}/query",
            json={
                "question": question
            },
            timeout=120,
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:

        return {
            "error": str(error)
        }


# ============================================================
# UI
# ============================================================

render_header()


# ------------------------------------------------------------
# API Status
# ------------------------------------------------------------

api_running = check_api()

render_api_status(api_running)


# ------------------------------------------------------------
# Knowledge Base
# ------------------------------------------------------------

render_knowledge_base()


# ------------------------------------------------------------
# Ingestion
# ------------------------------------------------------------

if render_ingest_button(api_running):

    with st.spinner("Ingesting documents..."):

        result = ingest_documents()

    if "error" in result:

        st.error(
            f"Ingestion failed: {result['error']}"
        )

    else:

        chunks = result.get(
            "chunks_created",
            "unknown",
        )

        st.success(
            f"Documents ingested successfully · "
            f"{chunks} chunks created"
        )


st.divider()


# ------------------------------------------------------------
# Question
# ------------------------------------------------------------

question = render_question_input()


# ------------------------------------------------------------
# Buttons
# ------------------------------------------------------------

ask_clicked, clear_clicked = render_question_buttons(
    api_running
)


if clear_clicked:

    st.rerun()


# ------------------------------------------------------------
# Query
# ------------------------------------------------------------

if ask_clicked:

    if not question.strip():

        st.warning(
            "Please enter a question first."
        )

    else:

        with st.spinner(
            "Searching your knowledge base..."
        ):

            result = ask_question(
                question.strip()
            )

        if "error" in result:

            st.error(
                f"Query failed: {result['error']}"
            )

        else:

            answer = result.get(
                "answer",
                "No answer returned.",
            )

            render_answer(answer)


# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

render_footer()