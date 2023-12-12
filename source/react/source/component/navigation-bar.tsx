import { useState } from "react";

import logo from "./../public/image/logo-original.png";


export const NavigationBar = () => {
    const [toggle, setToggle] = useState(false)

    return (
        <nav className="navbar is-fixed-top has-shadow" role="navigation" aria-label="main navigation">
            <div className="navbar-brand">
                <a className="navbar-item" href="/document">
                    <img className="mr-2" src={logo}></img>
                    <h1 className="subtitle has-text-info">Signature</h1>
                </a>

                <a role="button" className={`navbar-burger ${toggle ? "is-active" : ""}`} onClick={() => { setToggle(!toggle) }}>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                </a>
            </div>

            <div className={`navbar-menu ${toggle ? "is-active" : ""}`}>
                <div className="navbar-start">
                    <a className="navbar-item" href="/document">
                        <h1 className="subtitle">
                            Document
                        </h1>
                    </a>
                </div>

                <div className="navbar-end">
                    <a className="navbar-item" href="/profile">
                        <h1 className="subtitle">
                            <span className="icon mr-1 is-medium">
                                <i className="fas fa-lg fa-user-circle"></i>
                            </span>

                            <span>Profile</span>
                        </h1>
                    </a>
                </div>
            </div>
        </nav>
    )
}