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
    created_at: string;
    updated_at: string;
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

                <div className="columns is-multiline">
                    {documents.length > 0 ? (
                        documents.map((document: Document) => (
                            <div className="column is-one-quarter">
                                <div className="card">
                                    <div className="card-content">
                                        <div className="media">
                                            <div className="media-content">
                                                <p className="title is-4">
                                                    {document.title}
                                                </p>

                                                <p className="subtitle is-6 mb-2">
                                                    {`${document.code} - ${document.category}`}
                                                </p>

                                                <p className="subtitle is-7">
                                                    {
                                                        document.author_extend
                                                            .username
                                                    }
                                                </p>
                                            </div>
                                        </div>

                                        <div className="content">
                                            {document.description}
                                            <br />
                                            {new Date(
                                                document.created_at
                                            ).toLocaleDateString("en-GB")}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))
                    ) : (
                        <div>Data Not Found</div>
                    )}
                </div>
            </div>
        </section>
    );
};
