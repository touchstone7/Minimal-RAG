const API_BASE_URL = "http://127.0.0.1:8000";


// ============================================================
// HEALTH CHECK
// ============================================================

export async function checkApiHealth() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/health`
        );

        if (!response.ok) {
            throw new Error(
                `Health check failed: ${response.status}`
            );
        }

        return await response.json();

    } catch (error) {

        console.error(
            "API health check failed:",
            error
        );

        throw error;
    }
}


// ============================================================
// QUERY RAG
// ============================================================

export async function queryRag(question) {

    try {

        const response = await fetch(
            `${API_BASE_URL}/query`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({
                    question: question,
                }),
            }
        );

        if (!response.ok) {

            throw new Error(
                `Query failed: ${response.status}`
            );
        }

        return await response.json();

    } catch (error) {

        console.error(
            "RAG query failed:",
            error
        );

        throw error;
    }
}


// ============================================================
// INGEST DOCUMENT
// ============================================================

export async function ingestDocument(file) {

    try {

        const formData = new FormData();

        formData.append(
            "file",
            file
        );

        const response = await fetch(
            `${API_BASE_URL}/ingest`,
            {
                method: "POST",

                body: formData,
            }
        );

        if (!response.ok) {

            let errorMessage =
                `Ingestion failed: ${response.status}`;

            try {

                const errorData =
                    await response.json();

                if (errorData.detail) {
                    errorMessage =
                        errorData.detail;
                }

            } catch {
                // Ignore JSON parsing failure.
            }

            throw new Error(
                errorMessage
            );
        }

        return await response.json();

    } catch (error) {

        console.error(
            "Document ingestion failed:",
            error
        );

        throw error;
    }
}