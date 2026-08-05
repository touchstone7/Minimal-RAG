import {
    Check,
    Upload,
} from "lucide-react";


export default function IngestPanel({
    isOnline,
    ingesting,
    ingestionStatus,
    onIngest,
}) {


    function handleFileChange(event) {

        const file =
            event.target.files?.[0];


        if (file) {

            onIngest(file);

        }


        // Allow selecting the same file again later.

        event.target.value = "";
    }


    const uploadDisabled =
        !isOnline ||
        ingesting;


    return (

        <section className="ingestion-panel">


            {/* =====================================================
                SECTION HEADER
            ===================================================== */}

            <div className="ingestion-header">

                <div>

                    <div className="ingestion-label">
                        KNOWLEDGE BASE
                    </div>


                    <p className="ingestion-description">
                        Add documents to your local knowledge base.
                    </p>

                </div>

            </div>


            {/* =====================================================
                UPLOAD AREA
            ===================================================== */}

            <div className="ingestion-upload-area">


                <div className="ingestion-upload-copy">

                    <div className="ingestion-upload-title">
                        Add a document
                    </div>


                    <div className="ingestion-hint">
                        TXT · Markdown · PDF · DOCX
                    </div>

                </div>


                <div className="ingestion-controls">

                    <input
                        id="rag-file-upload"
                        type="file"
                        accept=".txt,.md,.pdf,.docx"
                        disabled={uploadDisabled}
                        onChange={handleFileChange}
                    />


                    <label
                        htmlFor="rag-file-upload"
                        className={
                            uploadDisabled
                                ? "ingest-button disabled"
                                : "ingest-button"
                        }
                    >

                        <Upload size={14} />


                        {
                            ingesting
                                ? "INGESTING..."
                                : "ADD DOCUMENT"
                        }

                    </label>

                </div>

            </div>


            {/* =====================================================
                INGESTION RESULT
            ===================================================== */}

            {ingestionStatus && (

                <div
                    className={
                        ingestionStatus.success
                            ? "ingestion-result success"
                            : "ingestion-result error"
                    }
                >


                    {ingestionStatus.success ? (

                        <>

                            <div className="ingestion-result-heading">

                                <Check size={15} />

                                <span>
                                    DOCUMENT ADDED
                                </span>

                            </div>


                            <div className="ingestion-result-file">

                                {ingestionStatus.filename}

                            </div>


                            <div className="ingestion-result-stats">

                                <div>
                                    +
                                    {
                                        ingestionStatus.chunksAdded
                                    }
                                    {" "}chunks added
                                </div>


                                <div>
                                    {
                                        ingestionStatus.totalChunks
                                    }
                                    {" "}total chunks
                                </div>

                            </div>

                        </>

                    ) : (

                        <div className="ingestion-result-error">

                            {ingestionStatus.message}

                        </div>

                    )}

                </div>

            )}

        </section>
    );
}