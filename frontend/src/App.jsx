import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import DashboardPage from "./pages/Dashboard.jsx";
import LoginPage from "./pages/LoginPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginPage />} />
        
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="*" element={<div className="p-10 text-center">404: Page Not Found</div>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;