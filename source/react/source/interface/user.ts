export default interface IUser {
    _id: number;
    name: string;
    username: string;
    email: string;
    password: string;
    role: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}
