import axios from "axios";
import { ReactElement, useEffect, useState } from "react";

import { IFormatResponse } from "../interface/format-response";
import { IDocument, IDocumentTotal } from "../interface/document";

import { CDocuments } from "../component/documents";
import { CPagination } from "../component/pagination";

export const Document = (): ReactElement => {
    const [count, setcount] = useState<number>(12);
    const [page, setPage] = useState<number>(1);
    const [documents, setDocuments] = useState<IDocument[]>([]);
    const [total, setTotal] = useState<number>(1);
    const [totalPage, setTotalPage] = useState<number>(1);

    const fetchDocument = async (): Promise<void> => {
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

    const fetchTotal = async (): Promise<void> => {
        const response = await axios<IFormatResponse<IDocumentTotal>>({
            method: "get",
            url: "https://signature-api.irswanda.com/api/document/count",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (response.data.success) {
            const newTotalPage: number = Math.ceil(
                response.data.data.total / count
            );

            setTotal(response.data.data.total);
            setTotalPage(newTotalPage);

            if (count > response.data.data.total) {
                setcount(response.data.data.total);
            }

            if (page > newTotalPage) {
                setPage(newTotalPage);
            }
        } else {
            setTotalPage(0);
        }
    };

    const decreaseCount = (): void => {
        setcount(count - 1);
    };

    const increaseCount = (): void => {
        setcount(count + 1);
    };

    const previousPage = (): void => {
        setPage(page - 1);
    };

    const nextPage = (): void => {
        setPage(page + 1);
    };

    useEffect((): void => {
        fetchDocument();
    }, [count, page]);

    useEffect((): void => {
        fetchTotal();
    }, [count]);

    return (
        <section className="section">
            <div className="container">
                <h1 className="title">Document</h1>

                <CPagination
                    page={page}
                    totalPage={totalPage}
                    previousPage={previousPage}
                    nextPage={nextPage}
                    count={count}
                    total={total}
                    decreaseCount={decreaseCount}
                    increaseCount={increaseCount}
                />

                {documents.length > 0 ? (
                    <CDocuments documents={documents} />
                ) : (
                    <div>Data Not Found</div>
                )}
            </div>
        </section>
    );
};
