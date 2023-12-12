import { Routes, Route } from "react-router-dom";

import { NavigationBar } from "./component/navigation-bar.tsx";
import { Document } from "./page/document.tsx";
import { Profile } from "./page/profile.tsx";

export const App = () => {
  return (
    <div className="App">
      <NavigationBar></NavigationBar>

      <Routes>
        <Route path="/document" element={<Document></Document>}></Route>
        <Route path="/profile" element={<Profile></Profile>}></Route>
      </Routes>
    </div>
  );
}