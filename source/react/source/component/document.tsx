import { IDocument } from "../interface/document";

export const CDocument: React.FC<{
    document: IDocument;
}> = ({ document }) => {
    return (
        <div className="column is-one-third">
            <div className="card">
                <div className="card-content">
                    <div className="media">
                        <div className="media-content">
                            <p className="title is-4">{document.title}</p>

                            <p className="subtitle is-6 mb-2">
                                {`${document.code} - ${document.category}`}
                            </p>

                            <p className="subtitle is-7">
                                {document.author_extend.username}
                            </p>
                        </div>
                    </div>

                    <div className="content">
                        {document.description}
                        <br />
                        {new Date(document.created_at).toLocaleDateString(
                            "en-GB"
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};
