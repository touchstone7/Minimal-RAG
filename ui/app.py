import requests
import streamlit as st


# ============================================================
# Configuration
# ============================================================

API_URL = "http://127.0.0.1:8000"


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="Minimal RAG",
    page_icon="🧠",
    layout="centered",
)


# ============================================================
# Header
# ============================================================

st.title("🧠 Minimal RAG")
st.write(
    "Ask questions about the documents indexed by the RAG system."
)


# ============================================================
# API Health Check
# ============================================================

try:

    response = requests.get(
        f"{API_URL}/health",
        timeout=5
    )

    if response.status_code == 200:

        st.success("RAG API is running")

    else:

        st.error("RAG API is not responding correctly.")

except requests.RequestException:

    st.error(
        "Could not connect to the FastAPI server. "
        "Make sure Uvicorn is running."
    )


st.divider()


# ============================================================
# Document Ingestion
# ============================================================

st.subheader("📚 Document Ingestion")

st.write(
    "Ingest the documents currently present in the project's data directory."
)

if st.button("Ingest Documents"):

    with st.spinner("Ingesting documents..."):

        try:

            response = requests.post(
                f"{API_URL}/ingest",
                timeout=300
            )

            if response.status_code == 200:

                result = response.json()

                st.success("Documents ingested successfully.")

                st.write(
                    f"Created **{result['chunks_created']} chunks**."
                )

            else:

                st.error(
                    f"Ingestion failed. "
                    f"HTTP {response.status_code}"
                )

                st.code(response.text)

        except requests.RequestException as error:

            st.error(
                "Could not connect to the FastAPI server."
            )

            st.code(str(error))


st.divider()


# ============================================================
# Question / Answer
# ============================================================

st.subheader("💬 Ask a Question")

question = st.text_input(
    "Enter your question:",
    placeholder="How does CPU handle memory usage?"
)


if st.button("Ask"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    f"{API_URL}/query",
                    json={
                        "question": question
                    },
                    timeout=300
                )

                if response.status_code == 200:

                    result = response.json()

                    st.subheader("Answer")

                    st.write(result["answer"])

                else:

                    st.error(
                        f"Query failed. "
                        f"HTTP {response.status_code}"
                    )

                    st.code(response.text)

            except requests.RequestException as error:

                st.error(
                    "Could not connect to the FastAPI server."
                )

                st.code(str(error))