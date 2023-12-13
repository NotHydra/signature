import { Routes, Route } from "react-router-dom";
import { ReactElement } from "react";

import { CNavigationBar } from "./component/navigation-bar.tsx";
import { Document } from "./page/document.tsx";
import { User } from "./page/user.tsx";

export const App = (): ReactElement => {
    return (
        <div className="App">
            <CNavigationBar />

            <Routes>
                <Route path="/" element={<Document />}></Route>
                <Route path="/document" element={<Document />}></Route>
                <Route path="/user" element={<User />}></Route>
            </Routes>
        </div>
    );
};
