import { IUser } from "../interface/user";

export const CUser: React.FC<{
    user: IUser;
}> = ({ user }) => {
    return (
        <div className="column is-one-quarter">
            <div className="card">
                <div className="card-content">
                    <div className="media">
                        <div className="media-content">
                            <p className="title is-4">{user.name}</p>

                            <p className="subtitle is-6 mb-2">
                                {`${user.username} - ${user.email}`}
                            </p>

                            <p className="subtitle is-7">
                                {user.role.toUpperCase()}
                            </p>
                        </div>
                    </div>

                    <div className="content">
                        {new Date(user.created_at).toLocaleDateString("en-GB")}
                    </div>
                </div>
            </div>
        </div>
    );
};
