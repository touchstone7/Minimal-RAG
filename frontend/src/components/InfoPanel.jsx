import {
    Database,
    Search,
    Cpu,
    X,
} from "lucide-react";


export default function InfoPanel({
    type,
    onClose,
}) {

    if (!type) {
        return null;
    }


    const content = {

        knowledge: {

            icon: <Database size={18} />,

            title: "KNOWLEDGE",

            rows: [

                ["VECTOR STORE", "ChromaDB"],

                ["EMBEDDINGS", "768 DIM"],

                ["STATUS", "LOCAL"],
            ],
        },


        retrieval: {

            icon: <Search size={18} />,

            title: "RETRIEVAL",

            rows: [

                ["STRATEGY", "SEMANTIC"],

                ["TOP K", "5"],

                ["PIPELINE", "RAG"],
            ],
        },


        system: {

            icon: <Cpu size={18} />,

            title: "SYSTEM",

            rows: [

                ["API", "FASTAPI"],

                ["LLM", "QWEN 3 8B"],

                ["INFERENCE", "OLLAMA"],
            ],
        },

    };


    const selected =
        content[type];


    return (

        <div className="info-panel">

            <div className="panel-header">

                <div className="panel-title">

                    {selected.icon}

                    {selected.title}

                </div>


                <button
                    className="icon-button"
                    onClick={onClose}
                >

                    <X size={16} />

                </button>

            </div>


            <div className="panel-content">

                {selected.rows.map(
                    ([label, value]) => (

                        <div
                            className="info-row"
                            key={label}
                        >

                            <span>
                                {label}
                            </span>

                            <strong>
                                {value}
                            </strong>

                        </div>

                    )
                )}

            </div>

        </div>
    );
}