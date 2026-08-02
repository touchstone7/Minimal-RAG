import streamlit as st


# ============================================================
# Header
# ============================================================

def render_header():
    st.caption("LOCAL RETRIEVAL-AUGMENTED GENERATION")

    st.title("Minimal RAG")

    st.write(
        "Ask questions about your own documents. "
        "Minimal RAG retrieves relevant context from your "
        "knowledge base and generates grounded answers."
    )

    st.divider()


# ============================================================
# API Status
# ============================================================

def render_api_status(is_running: bool):

    if is_running:

        st.markdown(
            '<div class="status-running">'
            '● &nbsp; RAG API is running'
            '</div>',
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            '<div class="status-offline">'
            '● &nbsp; RAG API is offline'
            '</div>',
            unsafe_allow_html=True,
        )

    st.write("")


# ============================================================
# Knowledge Base
# ============================================================

def render_knowledge_base():

    st.subheader("📚 Knowledge Base")

    st.write(
        "Load your configured documents into the RAG pipeline."
    )

    st.markdown(
        """
        <div class="knowledge-card">

        <div class="knowledge-title">
        📄 &nbsp; Existing document collection
        </div>

        <div class="knowledge-description">
        Documents from your configured data directory will be
        chunked, embedded and indexed in ChromaDB.
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")


# ============================================================
# Ingest Button
# ============================================================

def render_ingest_button(api_running: bool):

    return st.button(
        "↻  Ingest Documents",
        disabled=not api_running,
    )


# ============================================================
# Question Section
# ============================================================

def render_question_input():

    st.subheader("💬 Ask your knowledge base")

    st.write(
        "Ask a question and the RAG pipeline will retrieve "
        "relevant context before generating an answer."
    )

    question = st.text_area(
        "Question",
        placeholder=(
            "Ask something about the documents...\n\n"
            "Example: What does the document say about "
            "memory management?"
        ),
        height=140,
        label_visibility="collapsed",
    )

    return question


# ============================================================
# Question Buttons
# ============================================================

def render_question_buttons(api_running: bool):

    col1, col2, col3 = st.columns([1, 1, 3])

    with col1:

        ask_clicked = st.button(
            "Ask  →",
            disabled=not api_running,
            use_container_width=True,
        )

    with col2:

        clear_clicked = st.button(
            "Clear",
            use_container_width=True,
        )

    return ask_clicked, clear_clicked


# ============================================================
# Answer
# ============================================================

def render_answer(answer: str):

    st.write("")

    st.markdown(
        """
        <div class="answer-card">

        <div class="answer-label">
        ANSWER
        </div>

        <div class="answer-text">
        """,
        unsafe_allow_html=True,
    )

    st.write(answer)

    st.markdown(
        """
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Footer
# ============================================================

def render_footer():

    st.divider()

    st.markdown(
        """
        <div class="footer-text">
        Minimal RAG &nbsp; · &nbsp;
        Streamlit &nbsp; · &nbsp;
        FastAPI &nbsp; · &nbsp;
        ChromaDB &nbsp; · &nbsp;
        Ollama
        </div>
        """,
        unsafe_allow_html=True,
    )