import IUser from "../interface/user";

import { CUser } from "./user";

export const CUsers: React.FC<{
    users: IUser[];
}> = ({ users }) => {
    return (
        <div className="columns is-multiline">
            {users.map((user: IUser) => (
                <CUser key={user._id} user={user} />
            ))}
        </div>
    );
};
