import { ReactElement, useState } from "react";

import logo from "./../public/image/logo-original.png";

export const CNavigationBar = (): ReactElement => {
    const [toggle, setToggle] = useState<boolean>(false);

    return (
        <nav
            className="navbar is-fixed-top has-shadow"
            role="navigation"
            aria-label="main navigation"
        >
            <div className="navbar-brand">
                <a className="navbar-item" href="/document">
                    <img className="mr-2" src={logo} />
                    <h4 className="title is-4 has-text-info">Signature</h4>
                </a>

                <a
                    role="button"
                    className={`navbar-burger ${toggle ? "is-active" : ""}`}
                    onClick={() => {
                        setToggle(!toggle);
                    }}
                >
                    <span aria-hidden="true" />
                    <span aria-hidden="true" />
                    <span aria-hidden="true" />
                </a>
            </div>

            <div className={`navbar-menu ${toggle ? "is-active" : ""}`}>
                <div className="navbar-start">
                    <a className="navbar-item" href="/document">
                        <h4 className="subtitle">Document</h4>
                    </a>

                    <a className="navbar-item" href="/user">
                        <h4 className="subtitle">User</h4>
                    </a>
                </div>
            </div>
        </nav>
    );
};
