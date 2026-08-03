import { useState } from "react";


function QueryPanel({ onQuery, loading }) {

    const [question, setQuestion] = useState("");


    function handleSubmit(event) {
        event.preventDefault();

        if (!question.trim() || loading) {
            return;
        }

        onQuery(question);

        setQuestion("");
    }


    function handleKeyDown(event) {

        // Enter = submit
        // Shift + Enter = new line
        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {
            event.preventDefault();
            handleSubmit(event);
        }
    }


    return (
        <form
            className="query-area"
            onSubmit={handleSubmit}
        >

            <textarea
                className="query-box"
                value={question}
                onChange={(event) =>
                    setQuestion(event.target.value)
                }
                onKeyDown={handleKeyDown}
                placeholder="Ask something about your documents..."
                disabled={loading}
            />

            <div className="query-controls">

                <span className="query-hint">
                    ENTER TO QUERY · SHIFT + ENTER FOR NEW LINE
                </span>

                <button
                    type="submit"
                    className="query-button"
                    disabled={
                        loading ||
                        !question.trim()
                    }
                >
                    {loading ? "QUERYING..." : "QUERY →"}
                </button>

            </div>

        </form>
    );
}


export default QueryPanel;