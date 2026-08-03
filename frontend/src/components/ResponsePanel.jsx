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

        await navigator.clipboard.writeText(
            answer
        );
    }


    return (

        <section className="response-section">

            <div className="response-heading">

                <div>

                    <div className="eyebrow">
                        GENERATED RESPONSE
                    </div>

                    <div className="response-title">

                        <Sparkles size={15} />

                        RAG OUTPUT

                    </div>

                </div>


                <button
                    className="copy-button"
                    onClick={copyAnswer}
                >

                    <Copy size={14} />

                    COPY

                </button>

            </div>


            <div className="response-card">

                {answer}

            </div>

        </section>
    );
}