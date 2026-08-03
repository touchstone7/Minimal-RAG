import { useEffect, useState } from "react";

import Background from "./components/Background";
import Header from "./components/Header";
import QueryPanel from "./components/QueryPanel";
import ResponsePanel from "./components/ResponsePanel";

import { checkApiHealth, queryRag } from "./api/ragApi";


function App() {
    const [isOnline, setIsOnline] = useState(false);
    const [answer, setAnswer] = useState("");
    const [loading, setLoading] = useState(false);


    // ---------------------------------------------------------
    // Check whether FastAPI backend is available
    // ---------------------------------------------------------
    useEffect(() => {
        async function checkBackend() {
            try {
                await checkApiHealth();
                setIsOnline(true);
            } catch (error) {
                console.error("Backend health check failed:", error);
                setIsOnline(false);
            }
        }

        checkBackend();
    }, []);


    // ---------------------------------------------------------
    // Send user's question to RAG backend
    // ---------------------------------------------------------
    async function handleQuery(question) {
        if (!question.trim()) {
            return;
        }

        setLoading(true);
        setAnswer("");

        try {
            const result = await queryRag(question);

            // Adjust this if your API returns a different field.
            setAnswer(
                result.answer ||
                result.response ||
                "No answer was returned."
            );

        } catch (error) {
            console.error("RAG query failed:", error);

            setAnswer(
                "Unable to get a response from the RAG backend."
            );

        } finally {
            setLoading(false);
        }
    }


    return (
        <div className="app">

            <Background />

            <div className="app-content">

                <Header isOnline={isOnline} />

                <main className="main">

                    <section className="hero">

                        <div className="eyebrow">
                            KNOWLEDGE INTERFACE
                        </div>

                        <h1 className="hero-title">
                            Ask your knowledge base.
                        </h1>

                        <p className="hero-description">
                            Retrieve relevant context from your documents
                            and generate an answer using your local
                            language model.
                        </p>

                        <QueryPanel
                            onQuery={handleQuery}
                            loading={loading}
                        />

                        <ResponsePanel
                            answer={answer}
                            loading={loading}
                        />

                    </section>

                </main>

                <footer className="footer">

                    <span>
                        MINIMAL-RAG / LOCAL INFERENCE
                    </span>

                    <span className="footer-right">

                        <span
                            className={
                                isOnline
                                    ? "footer-online"
                                    : ""
                            }
                        >
                            ● RAG {isOnline ? "ONLINE" : "OFFLINE"}
                        </span>

                    </span>

                </footer>

            </div>

        </div>
    );
}


// IMPORTANT:
// main.jsx imports App as:
// import App from "./App.jsx";
//
// Therefore App.jsx MUST have a default export.
export default App;