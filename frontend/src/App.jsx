import { useEffect, useState } from "react";
import axios from "axios";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

import "./App.css";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Header from "./components/Header";
import UploadCard from "./components/UploadCard";
import AnalysisCard from "./components/AnalysisCard";
import DashboardCards from "./components/DashboardCards";
import SearchFilter from "./components/SearchFilter";
import HistoryTable from "./components/HistoryTable";
import RiskAnalytics from "./components/RiskAnalytics";

const API = "http://127.0.0.1:8000";

const COLORS = [
  "#ef4444",
  "#dc2626",
  "#facc15",
  "#22c55e",
];

function App() {

  // ===========================
  // States
  // ===========================

  const [file, setFile] = useState(null);

  const [analysis, setAnalysis] = useState(null);

  const [dashboard, setDashboard] = useState(null);

  const [history, setHistory] = useState([]);

  const [filteredHistory, setFilteredHistory] = useState([]);

  const [loading, setLoading] = useState(false);

  const [search, setSearch] = useState("");

  const [riskFilter, setRiskFilter] = useState("All");


  // ===========================
  // Dashboard
  // ===========================

  const loadDashboard = async () => {

    try {

      const res = await axios.get(
        `${API}/dashboard`
      );

      setDashboard(res.data);

    } catch (err) {

      console.error(err);

    }

  };


  // ===========================
  // History
  // ===========================

  const loadHistory = async () => {

    try {

      const res = await axios.get(
        `${API}/history`
      );

      setHistory(res.data);

      setFilteredHistory(res.data);

    } catch (err) {

      console.error(err);

    }

  };


  // ===========================
  // Initial Load
  // ===========================

  useEffect(() => {

    loadDashboard();

    loadHistory();

  }, []);


  // ===========================
  // Search + Filter
  // ===========================

  useEffect(() => {

    let data = [...history];

    // Search

    if (search.trim() !== "") {

      data = data.filter((item) =>
        item.filename
          .toLowerCase()
          .includes(search.toLowerCase())
      );

    }

    // Risk Filter

    if (riskFilter !== "All") {

      data = data.filter(
        (item) =>
          item.risk_level.toLowerCase() ===
          riskFilter.toLowerCase()
      );

    }

    setFilteredHistory(data);

  }, [search, riskFilter, history]);


  // ===========================
  // Analyze Log
  // ===========================

  const analyzeLog = async () => {

    if (!file) {

      toast.warning("Please choose a log file.");

      return;

    }

    const formData = new FormData();

    formData.append("file", file);

    try {

      setLoading(true);

      const res = await axios.post(

        `${API}/upload-log`,

        formData

      );

      setAnalysis(res.data.analysis);

      await loadDashboard();

      await loadHistory();

      toast.success("Analysis completed successfully.");


    } catch (err) {

      console.error(err);

      toast.error(
        err.response?.data?.detail ||
        err.message
      );

    }

    finally {

      setLoading(false);

    }

  };


  // ===========================
  // Delete Analysis
  // ===========================

  const deleteAnalysis = async (id) => {

    const confirmDelete = window.confirm(

      "Delete this analysis?"

    );

    if (!confirmDelete) return;

    try {

      await axios.delete(

        `${API}/analysis/${id}`

      );

      await loadDashboard();

      await loadHistory();

    } catch (err) {

      console.error(err);

      toast.error("Unable to delete.");

    }

  };


  // ===========================
  // Download Report
  // ===========================

  const downloadReport = (id) => {

    window.open(

      `${API}/download-report/${id}`,

      "_blank"

    );

  };


  // ===========================
  // Charts
  // ===========================

  const pieData = [

    {
      name: "Critical",
      value: dashboard?.critical_risk || 0,
    },

    {
      name: "High",
      value: dashboard?.high_risk || 0,
    },

    {
      name: "Medium",
      value: dashboard?.medium_risk || 0,
    },

    {
      name: "Low",
      value: dashboard?.low_risk || 0,
    },

  ];

  const barData = [

    {
      risk: "Critical",
      count: dashboard?.critical_risk || 0,
    },

    {
      risk: "High",
      count: dashboard?.high_risk || 0,
    },

    {
      risk: "Medium",
      count: dashboard?.medium_risk || 0,
    },

    {
      risk: "Low",
      count: dashboard?.low_risk || 0,
    },

  ];

  return (

    <div className="container">

      <Header />

      <UploadCard
        setFile={setFile}
        analyzeLog={analyzeLog}
        loading={loading}
      />

      <AnalysisCard
        analysis={analysis}
        dashboard={dashboard}
        downloadReport={downloadReport}
      />

      <DashboardCards
        dashboard={dashboard}
      />

      <RiskAnalytics
        pieData={pieData}
        barData={barData}
        COLORS={COLORS}
      />

      <SearchFilter
        search={search}
        setSearch={setSearch}
        riskFilter={riskFilter}
        setRiskFilter={setRiskFilter}
      />

      <HistoryTable
        filteredHistory={filteredHistory}
        downloadReport={downloadReport}
        deleteAnalysis={deleteAnalysis}
      />

      <ToastContainer
        position="top-right"
        autoClose={3000}
        theme="dark"
      />

    </div>
  );
}

export default App;