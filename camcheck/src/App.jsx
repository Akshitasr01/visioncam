import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Monitor from "./pages/Monitor";
import Alerts from "./pages/Alerts";
import Dashboard from "./pages/Dashboard";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/monitor" element={<Monitor />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
