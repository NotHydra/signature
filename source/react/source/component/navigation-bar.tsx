import logo from "./../public/image/logo-original.png";


export const NavigationBar = () => {
    return (
        <nav className="navbar" role="navigation" aria-label="main navigation">
            <div className="navbar-brand">
                <a className="navbar-item" href="/document">
                    <img className="mr-2" src={logo}></img>

                    <h1 className="subtitle has-text-info">Signature</h1>
                </a>

                <a role="button" className="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                </a>
            </div>

            <div id="navbarBasicExample" className="navbar-menu">
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
                            Profile
                        </h1>
                    </a>
                </div>
            </div>
        </nav>
    )
}