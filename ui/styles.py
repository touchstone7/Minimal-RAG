import streamlit as st


def load_styles():
    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL
        ===================================================== */

        .stApp {
            background-color: #0b0f14;
            color: #e6edf3;
        }

        .main .block-container {
            max-width: 1000px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }

        /* Hide Streamlit branding */
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        /* =====================================================
           TYPOGRAPHY
        ===================================================== */

        h1 {
            letter-spacing: -0.04em;
        }

        h2 {
            letter-spacing: -0.025em;
        }

        /* =====================================================
           BUTTONS
        ===================================================== */

        .stButton > button {
            border-radius: 8px;
            min-height: 42px;

            background-color: #151b23;
            border: 1px solid #30363d;

            color: #e6edf3;

            font-weight: 600;
            transition: all 0.15s ease;
        }

        .stButton > button:hover {
            border-color: #58a6ff;
            background-color: #1c2128;
            color: #ffffff;
        }

        /* =====================================================
           TEXT AREA
        ===================================================== */

        textarea {
            background-color: #11161d !important;
            color: #e6edf3 !important;

            border: 1px solid #30363d !important;
            border-radius: 10px !important;
        }

        textarea:focus {
            border-color: #58a6ff !important;
            box-shadow: 0 0 0 1px #58a6ff !important;
        }

        /* =====================================================
           DIVIDERS
        ===================================================== */

        hr {
            border-color: #21262d !important;
        }

        /* =====================================================
           ALERTS
        ===================================================== */

        [data-testid="stAlert"] {
            border-radius: 9px;
        }

        /* =====================================================
           SPINNER
        ===================================================== */

        [data-testid="stSpinner"] {
            color: #58a6ff;
        }

        /* =====================================================
           STATUS
        ===================================================== */

        .status-running {
            padding: 0.75rem 1rem;
            border-radius: 8px;

            background-color: #0f2419;
            border: 1px solid #1f6f43;

            color: #7ee2a8;

            font-size: 0.9rem;
            font-weight: 600;
        }

        .status-offline {
            padding: 0.75rem 1rem;
            border-radius: 8px;

            background-color: #251313;
            border: 1px solid #6e2525;

            color: #ff9b9b;

            font-size: 0.9rem;
            font-weight: 600;
        }

        /* =====================================================
           KNOWLEDGE BASE CARD
        ===================================================== */

        .knowledge-card {
            padding: 1.4rem;

            background-color: #11161d;
            border: 1px solid #252d38;
            border-radius: 12px;
        }

        .knowledge-title {
            font-size: 1rem;
            font-weight: 650;
            color: #f0f6fc;

            margin-bottom: 0.4rem;
        }

        .knowledge-description {
            color: #8b949e;
            font-size: 0.9rem;
            line-height: 1.6;
        }

        /* =====================================================
           ANSWER CARD
        ===================================================== */

        .answer-card {
            padding: 1.4rem;

            background-color: #11161d;
            border: 1px solid #252d38;
            border-radius: 12px;
        }

        .answer-label {
            color: #8b949e;

            font-size: 0.72rem;
            font-weight: 700;

            letter-spacing: 0.1em;
            text-transform: uppercase;

            margin-bottom: 0.8rem;
        }

        .answer-text {
            color: #e6edf3;

            font-size: 1rem;
            line-height: 1.75;
        }

        /* =====================================================
           FOOTER
        ===================================================== */

        .footer-text {
            text-align: center;

            color: #6e7681;
            font-size: 0.8rem;

            padding-top: 1rem;
            padding-bottom: 1rem;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )