import {
    Sparkles,
    Copy,
} from "lucide-react";


export default function ResponsePanel({
    answer,
}) {

    if (!answer) {
        return null;
    }


    async function copyAnswer() {

        try {

            await navigator.clipboard.writeText(
                answer
            );

        } catch (error) {

            console.error(
                "Failed to copy response:",
                error
            );
        }
    }


    return (

        <section className="response-section">


            {/* =====================================================
                RESPONSE HEADER
            ===================================================== */}

            <div className="response-heading">

                <div>

                    <div className="eyebrow">
                        GENERATED RESPONSE
                    </div>


                    <div className="response-title">

                        <Sparkles size={15} />

                        <span>
                            RAG OUTPUT
                        </span>

                    </div>

                </div>


                <button
                    type="button"
                    className="copy-button"
                    onClick={copyAnswer}
                >

                    <Copy size={14} />

                    <span>
                        COPY
                    </span>

                </button>

            </div>


            {/* =====================================================
                RESPONSE CONTENT
            ===================================================== */}

            <div className="response-card">

                <p className="response-text">
                    {answer}
                </p>

            </div>

        </section>
    );
}