import logo from "./logo.svg";
import "./App.css";
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import EntryPage from "./pages/EntryPage.jsx";
import Login from "./components/Login";
import SignUp from "./components/SignUp";
import "@coreui/coreui/dist/css/coreui.min.css";

function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<EntryPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
