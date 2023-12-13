import axios from "axios";
import { ReactElement, useEffect, useState } from "react";

import IFormatResponse from "../interface/format-response";
import IUser from "../interface/user";

import { CUsers } from "../component/users";

export const User = (): ReactElement => {
    const [users, setUsers] = useState<IUser[]>([]);

    useEffect(() => {
        (async () => {
            const response = await axios<IFormatResponse<IUser[]>>({
                method: "get",
                url: "https://signature-api.irswanda.com/api/user",
                headers: {
                    "Content-Type": "application/json",
                },
                params: {
                    count: 10,
                    page: 1,
                },
            });

            if (response.data.success) {
                setUsers(response.data.data);
            } else {
                setUsers([]);
            }
        })();
    }, []);

    return (
        <section className="section">
            <div className="container">
                <h1 className="title">User</h1>
                <p className="subtitle">{users.length} Total Users</p>

                {users.length > 0 ? (
                    <CUsers users={users} />
                ) : (
                    <div>Data Not Found</div>
                )}
            </div>
        </section>
    );
};
