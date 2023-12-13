import { TVoidFunction } from "../type/function";

export const CPagination: React.FC<{
    page: number;
    totalPage: number;
    previousPage: TVoidFunction;
    nextPage: TVoidFunction;
    count: number;
    total: number;
    decreaseCount: TVoidFunction;
    increaseCount: TVoidFunction;
}> = ({
    page,
    totalPage,
    previousPage,
    nextPage,
    count,
    total,
    decreaseCount,
    increaseCount,
}) => {
    return (
        <>
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
        </>
    );
};
