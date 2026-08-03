const API_BASE_URL = "http://127.0.0.1:8000";


/* =========================================================
   HEALTH CHECK
========================================================= */

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

        const data = await response.json();

        return data;

    } catch (error) {

        console.error(
            "API health check failed:",
            error
        );

        throw error;
    }
}


/* =========================================================
   QUERY RAG
========================================================= */

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

            const errorText =
                await response.text();

            console.error(
                "RAG backend error:",
                response.status,
                errorText
            );

            throw new Error(
                `Query failed: ${response.status} ${errorText}`
            );
        }


        const data =
            await response.json();

        return data;

    } catch (error) {

        console.error(
            "RAG query failed:",
            error
        );

        throw error;
    }
}