import axios from "axios";
import { ReactElement, useEffect, useState } from "react";

import { IFormatResponse } from "../interface/format-response";
import { IUser, IUserTotal } from "../interface/user";

import { CUsers } from "../component/users";

export const User = (): ReactElement => {
    const [users, setUsers] = useState<IUser[]>([]);
    const [total, setTotal] = useState<number>(0);

    const fetchUser = async () => {
        const response = await axios<IFormatResponse<IUser[]>>({
            method: "get",
            url: "https://signature-api.irswanda.com/api/user",
            headers: {
                "Content-Type": "application/json",
            },
            params: {
                count: 12,
                page: 1,
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
            setTotal(response.data.data.total);
        } else {
            setTotal(0);
        }
    };

    useEffect(() => {
        fetchUser();
        fetchTotal();
    }, []);

    return (
        <section className="section">
            <div className="container">
                <h1 className="title">User</h1>

                <p className="subtitle">
                    {users.length} out of {total} total users
                </p>

                {users.length > 0 ? (
                    <CUsers users={users} />
                ) : (
                    <div>Data Not Found</div>
                )}
            </div>
        </section>
    );
};
