import { Routes, Route } from "react-router-dom";
import { ReactElement } from "react";

import { NavigationBar } from "./component/navigation-bar.tsx";
import { Document } from "./page/document.tsx";
import { Profile } from "./page/profile.tsx";

export const App = (): ReactElement => {
  return (
    <div className="App">
      <NavigationBar />

      <Routes>
        <Route path="/" element={<Document />}></Route>
        <Route path="/document" element={<Document />}></Route>
        <Route path="/profile" element={<Profile />}></Route>
      </Routes>
    </div>
  );
}