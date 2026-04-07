import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import UserType from "./pages/UserType";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Monitor from "./pages/Monitor";
import Dashboard from "./pages/Dashboard";
import Alerts from "./pages/Alerts";
import Settings from "./pages/Settings";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Main */}
        <Route path="/" element={<Home />} />
        <Route path="/user-type" element={<UserType />} />

        {/* Auth */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Core App */}
        <Route path="/monitor" element={<Monitor />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </BrowserRouter>
  );
}
