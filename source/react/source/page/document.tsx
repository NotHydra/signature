import axios from "axios";
import { ReactElement, useEffect, useState } from "react";

import { IFormatResponse } from "../interface/format-response";
import { IDocument, IDocumentTotal } from "../interface/document";

import { CDocuments } from "../component/documents";

export const Document = (): ReactElement => {
    const count = 12;

    const [page, setPage] = useState<number>(1);
    const [documents, setDocuments] = useState<IDocument[]>([]);
    const [total, setTotal] = useState<number>(0);

    const fetchDocument = async () => {
        const response = await axios<IFormatResponse<IDocument[]>>({
            method: "get",
            url: "https://signature-api.irswanda.com/api/document",
            headers: {
                "Content-Type": "application/json",
            },
            params: {
                count: count,
                page: page,
            },
        });

        if (response.data.success) {
            setDocuments(response.data.data);
        } else {
            setDocuments([]);
        }
    };

    const fetchTotal = async () => {
        const response = await axios<IFormatResponse<IDocumentTotal>>({
            method: "get",
            url: "https://signature-api.irswanda.com/api/document/count",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (response.data.success) {
            setTotal(response.data.data.total);
        } else {
            setTotal(0);
        }
    };

    useEffect(() => {
        fetchDocument();
        fetchTotal();
    }, []);

    return (
        <section className="section">
            <div className="container">
                <h1 className="title">Document</h1>

                <p className="subtitle pb-0 mb-2">
                    Page {page} out of {Math.ceil(total / count)}
                </p>

                <div className="field has-addons">
                    <p className="control">
                        <button className="button button-custom-width">
                            <span className="icon is-small">
                                <i className="fas fa-chevron-left"></i>
                            </span>

                            <span>Previous</span>
                        </button>
                    </p>

                    <p className="control">
                        <button className="button button-custom-width">
                            <span>Next</span>

                            <span className="icon is-small">
                                <i className="fas fa-chevron-right"></i>
                            </span>
                        </button>
                    </p>
                </div>

                {documents.length > 0 ? (
                    <CDocuments documents={documents} />
                ) : (
                    <div>Data Not Found</div>
                )}
            </div>
        </section>
    );
};
