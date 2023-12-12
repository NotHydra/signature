import ReactDOM from 'react-dom/client'
import { BrowserRouter } from "react-router-dom";

import { App } from './App.tsx'

import "./public/css/index.css";

ReactDOM.createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
)
