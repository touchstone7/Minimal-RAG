import {
    Database,
    Activity,
    Cpu,
} from "lucide-react";


export default function Header({
    apiOnline,
    onOpenPanel,
}) {

    return (

        <header className="top-header">

            <div className="brand">

                <div className="brand-mark">
                    <Database size={17} />
                </div>

                <div>

                    <div className="brand-name">
                        MINIMAL-RAG
                    </div>

                    <div className="brand-subtitle">
                        RETRIEVAL INTELLIGENCE
                    </div>

                </div>

            </div>


            <nav className="navigation">

                <button
                    onClick={() =>
                        onOpenPanel("knowledge")
                    }
                >
                    KNOWLEDGE
                </button>


                <button
                    onClick={() =>
                        onOpenPanel("retrieval")
                    }
                >
                    RETRIEVAL
                </button>


                <button
                    onClick={() =>
                        onOpenPanel("system")
                    }
                >
                    SYSTEM
                </button>

            </nav>

        </header>
    );
}