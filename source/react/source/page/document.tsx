import axios from "axios";
import { ReactElement, useEffect, useState } from "react";

import FormatResponse from "../interface/format-response";

interface Document {
    _id: number;
    id_author: number;
    code: string;
    title: string;
    category: string;
    description: string;
    created_at: Date;
    updated_at: Date;
    author_extend: {
        username: string;
    };
}

export const Document = (): ReactElement => {
    const [documents, setDocuments] = useState<Document[]>([]);

    useEffect(() => {
        const fetchDocument = async () => {
            const response = await axios<FormatResponse<Document[]>>({
                method: "get",
                url: "https://signature-api.irswanda.com/api/document",
                headers: {
                    "Content-Type": "application/json",
                },
                params: {
                    count: 10,
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
                    documents.map((document: Document) => (
                        <p>{JSON.stringify(document)}</p>
                    ))
                ) : (
                    <p>Data Not Found</p>
                )}
            </div>
        </section>
    );
};
