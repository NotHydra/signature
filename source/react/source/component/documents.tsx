import IDocument from "../interface/document";

import { CDocument } from "./document";

export const CDocuments: React.FC<{
    documents: IDocument[];
}> = ({ documents }) => {
    return (
        <div className="columns is-multiline">
            {documents.map((document: IDocument) => (
                <CDocument key={document._id} document={document} />
            ))}
        </div>
    );
};
