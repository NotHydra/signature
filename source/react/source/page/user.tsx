import axios from "axios";
import { ReactElement, useEffect, useState } from "react";

import { IFormatResponse } from "../interface/format-response";
import { IUser, IUserTotal } from "../interface/user";

import { CUsers } from "../component/users";

export const User = (): ReactElement => {
    const [count, setcount] = useState<number>(12);
    const [page, setPage] = useState<number>(1);
    const [users, setUsers] = useState<IUser[]>([]);
    const [total, setTotal] = useState<number>(1);
    const [totalPage, setTotalPage] = useState<number>(1);

    const fetchUser = async () => {
        const response = await axios<IFormatResponse<IUser[]>>({
            method: "get",
            url: "https://signature-api.irswanda.com/api/user",
            headers: {
                "Content-Type": "application/json",
            },
            params: {
                count: count,
                page: page,
            },
        });

        if (response.data.success) {
            setUsers(response.data.data);
        } else {
            setUsers([]);
        }
    };

    const fetchTotal = async () => {
        const response = await axios<IFormatResponse<IUserTotal>>({
            method: "get",
            url: "https://signature-api.irswanda.com/api/user/count",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (response.data.success) {
            const newTotalPage = Math.ceil(response.data.data.total / count);

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
    const decreaseCount = () => {
        setcount(count - 1);
    };

    const increaseCount = () => {
        setcount(count + 1);
    };

    const previousPage = () => {
        setPage(page - 1);
    };

    const nextPage = () => {
        setPage(page + 1);
    };

    useEffect(() => {
        fetchUser();
    }, [count, page]);

    useEffect(() => {
        fetchTotal();
    }, [count]);

    return (
        <section className="section">
            <div className="container">
                <h1 className="title">User</h1>

                <p className="subtitle pb-0 mb-2">
                    Page {page} out of {totalPage}
                </p>

                <div className="columns">
                    <div className="column is-one-third">
                        <div className="field has-addons">
                            <p className="control is-expanded">
                                <button
                                    className="button is-fullwidth"
                                    disabled={page > 1 ? false : true}
                                    onClick={previousPage}
                                >
                                    <span className="icon is-small">
                                        <i className="fas fa-chevron-left"></i>
                                    </span>

                                    <span>Previous</span>
                                </button>
                            </p>

                            <p className="control is-expanded">
                                <button
                                    className="button is-fullwidth"
                                    disabled={page < totalPage ? false : true}
                                    onClick={nextPage}
                                >
                                    <span>Next</span>

                                    <span className="icon is-small">
                                        <i className="fas fa-chevron-right"></i>
                                    </span>
                                </button>
                            </p>
                        </div>

                        <div className="field has-addons">
                            <p className="control is-expanded">
                                <button
                                    className="button is-fullwidth"
                                    disabled={count > 1 ? false : true}
                                    onClick={decreaseCount}
                                >
                                    <span className="icon is-small">
                                        <i className="fas fa-minus"></i>
                                    </span>
                                </button>
                            </p>

                            <p className="control is-expanded">
                                <input
                                    className="input"
                                    type="number"
                                    value={count}
                                    readOnly
                                    style={{ textAlign: "center" }}
                                />
                            </p>

                            <p className="control is-expanded">
                                <button
                                    className="button is-fullwidth"
                                    disabled={count < total ? false : true}
                                    onClick={increaseCount}
                                >
                                    <span className="icon is-small">
                                        <i className="fas fa-plus"></i>
                                    </span>
                                </button>
                            </p>
                        </div>
                    </div>
                </div>

                {users.length > 0 ? (
                    <CUsers users={users} />
                ) : (
                    <div>Data Not Found</div>
                )}
            </div>
        </section>
    );
};
