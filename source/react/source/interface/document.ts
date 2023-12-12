export default interface IDocument {
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
