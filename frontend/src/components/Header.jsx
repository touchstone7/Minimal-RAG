import {
    Database,
} from "lucide-react";


export default function Header() {

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

        </header>
    );
}