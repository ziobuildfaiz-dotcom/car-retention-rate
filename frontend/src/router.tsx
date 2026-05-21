import { Routes, Route } from "react-router-dom";
import AppLayout from "./components/layout/AppLayout";
import Dashboard from "./pages/Dashboard";
import ModelDetail from "./pages/ModelDetail";
import BrandAnalysis from "./pages/BrandAnalysis";
import Comparison from "./pages/Comparison";
import DataExplorer from "./pages/DataExplorer";

export default function AppRouter() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/models/:id" element={<ModelDetail />} />
        <Route path="/brands/:id" element={<BrandAnalysis />} />
        <Route path="/compare" element={<Comparison />} />
        <Route path="/explore" element={<DataExplorer />} />
      </Route>
    </Routes>
  );
}
