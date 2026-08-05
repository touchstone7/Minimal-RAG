import { useEffect, useState } from "react";

import Background from "./components/Background";
import Header from "./components/Header";
import IngestPanel from "./components/IngestPanel";
import QueryPanel from "./components/QueryPanel";
import ResponsePanel from "./components/ResponsePanel";

import {
    checkApiHealth,
    queryRag,
    ingestDocument,
} from "./api/ragApi";


function App() {

    // =========================================================
    // BACKEND STATUS
    // =========================================================

    const [isOnline, setIsOnline] = useState(false);


    // =========================================================
    // QUERY STATE
    // =========================================================

    const [answer, setAnswer] = useState("");
    const [loading, setLoading] = useState(false);


    // =========================================================
    // INGESTION STATE
    // =========================================================

    const [ingesting, setIngesting] = useState(false);

    const [ingestionStatus, setIngestionStatus] =
        useState(null);


    // =========================================================
    // BACKEND HEALTH CHECK
    // =========================================================

    useEffect(() => {

        async function checkBackend() {

            try {

                await checkApiHealth();

                setIsOnline(true);

            } catch (error) {

                console.error(
                    "Backend health check failed:",
                    error
                );

                setIsOnline(false);
            }
        }


        checkBackend();


        const interval = setInterval(
            checkBackend,
            5000
        );


        return () => {
            clearInterval(interval);
        };

    }, []);


    // =========================================================
    // QUERY
    // =========================================================

    async function handleQuery(question) {

        if (!question?.trim()) {
            return;
        }


        setLoading(true);
        setAnswer("");


        try {

            const result =
                await queryRag(question);


            setAnswer(
                result.answer ||
                result.response ||
                "No answer was returned."
            );


        } catch (error) {

            console.error(
                "RAG query failed:",
                error
            );


            setAnswer(
                "Unable to get a response from the RAG backend."
            );

        } finally {

            setLoading(false);
        }
    }


    // =========================================================
    // DOCUMENT INGESTION
    // =========================================================

    async function handleIngest(file) {

        if (!file) {
            return;
        }


        setIngesting(true);
        setIngestionStatus(null);


        try {

            const result =
                await ingestDocument(file);


            setIngestionStatus({

                success: true,

                filename:
                    result.filename,

                chunksAdded:
                    result.chunks_added,

                totalChunks:
                    result.total_chunks,

            });


        } catch (error) {

            console.error(
                "Document ingestion failed:",
                error
            );


            setIngestionStatus({

                success: false,

                message:
                    error.message ||
                    "Unable to ingest the document.",

            });


        } finally {

            setIngesting(false);
        }
    }


    // =========================================================
    // UI
    // =========================================================

    return (

        <div className="app">

            <Background />


            <div className="app-content">

                <Header
                    apiOnline={isOnline}
                />


                <main className="main">

                    <section className="hero">


                        {/* =================================================
                            KNOWLEDGE BASE
                        ================================================= */}

                        <IngestPanel
                            isOnline={isOnline}
                            ingesting={ingesting}
                            ingestionStatus={ingestionStatus}
                            onIngest={handleIngest}
                        />


                        {/* =================================================
                            KNOWLEDGE INTERFACE
                        ================================================= */}

                        <section className="knowledge-interface">

                            <div className="eyebrow">
                                KNOWLEDGE INTERFACE
                            </div>


                            <h1 className="hero-title">
                                Ask your knowledge base.
                            </h1>


                            <p className="hero-description">
                                Retrieve relevant context from your
                                documents and generate an answer using
                                your local language model.
                            </p>


                            {/* -----------------------------------------
                                QUERY
                            ----------------------------------------- */}

                            <QueryPanel
                                onQuery={handleQuery}
                                loading={loading}
                            />


                            {/* -----------------------------------------
                                RESPONSE
                            ----------------------------------------- */}

                            <ResponsePanel
                                answer={answer}
                                loading={loading}
                            />

                        </section>

                    </section>

                </main>


                {/* =====================================================
                    FOOTER
                ===================================================== */}

                <footer className="footer">

                    <span>
                        MINIMAL-RAG / LOCAL INFERENCE
                    </span>


                    <span className="footer-right">

                        <span
                            className={
                                isOnline
                                    ? "footer-online"
                                    : "footer-offline"
                            }
                        >

                            ● RAG{" "}
                            {
                                isOnline
                                    ? "ONLINE"
                                    : "OFFLINE"
                            }

                        </span>

                    </span>

                </footer>

            </div>

        </div>
    );
}


export default App;