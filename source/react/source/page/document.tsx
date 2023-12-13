import axios from "axios";
import { ReactElement, useEffect, useState } from "react";

import IFormatResponse from "../interface/format-response";
import IDocument from "../interface/document";

import { CDocuments } from "../component/documents";

export const Document = (): ReactElement => {
    const [documents, setDocuments] = useState<IDocument[]>([]);

    useEffect(() => {
        const fetchDocument = async () => {
            const response = await axios<IFormatResponse<IDocument[]>>({
                method: "get",
                url: "https://signature-api.irswanda.com/api/document",
                headers: {
                    "Content-Type": "application/json",
                },
                params: {
                    count: 12,
                    page: 1,
                },
            });

            if (response.data.success) {
                setDocuments(response.data.data);
            } else {
                setDocuments([]);
            }
        };

        fetchDocument();
    }, []);

    return (
        <section className="section">
            <div className="container">
                <h1 className="title">Document</h1>
                <p className="subtitle">{documents.length} Total Documents</p>

                {documents.length > 0 ? (
                    <CDocuments documents={documents} />
                ) : (
                    <div>Data Not Found</div>
                )}
            </div>
        </section>
    );
};
