import { useEffect, useState } from "react";
import { fetchRfps, fetchLogs, fetchUser, triggerScraper, runSalesAgent, runMainAgent } from "../services/rfpApi";
import { Activity } from "lucide-react";

import Navbar from "../components/Navbar";
import StatsCard from "../components/StatsCard";
import AgentControlPanel from "../components/AgentControlPanel";
import RfpList from "../components/RfpList";

export default function DashboardPage() {
  const [rfps, setRfps] = useState([]);
  const [logs, setLogs] = useState([]);
  const [user, setUser] = useState({ username: "Guest", role: "Viewer" });
  
  const [filterStatus, setFilterStatus] = useState("ALL");
  const [searchTerm, setSearchTerm] = useState("");
  const [actionLoading, setActionLoading] = useState("");

  const refreshData = async () => {
    try {
      const [rfpData, logData] = await Promise.all([
        fetchRfps(filterStatus, searchTerm), 
        fetchLogs()
      ]);
      setRfps(rfpData.sort((a, b) => b.id - a.id));
      setLogs(logData);
    } catch (e) { console.error(e); }
  };

  useEffect(() => {
    fetchUser().then(setUser).catch(() => {});
  }, []);

  useEffect(() => {
    refreshData();
    const interval = setInterval(refreshData, 3000); 
    return () => clearInterval(interval);
  }, [filterStatus, searchTerm]);

  const handleAction = async (name) => {
    const apiMap = {
      "scraper": triggerScraper,
      "sales": runSalesAgent,
      "main": runMainAgent
    };
    
    setActionLoading(name);
    try {
      await apiMap[name]();
      setTimeout(refreshData, 1000);
    } catch (e) {
      alert("Action failed: " + e.message);
    } finally {
      setActionLoading("");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-800 flex flex-col">
      <Navbar user={user} />

      <div className="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-12 gap-8">
        
        {/* LEFT COLUMN: Sidebar */}
        <aside className="col-span-12 md:col-span-3 space-y-6">
          <StatsCard rfps={rfps} />
          <AgentControlPanel actionLoading={actionLoading} onAction={handleAction} />
          
          {/* Logs Component (Simple enough to keep inline or move later) */}
          <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 h-64 flex flex-col">
            <h3 className="text-xs font-bold text-gray-400 uppercase mb-3 flex items-center gap-2">
              <Activity size={14} /> Live System Logs
            </h3>
            <div className="flex-1 overflow-auto space-y-3 pr-2 custom-scrollbar">
              {logs.map((log, i) => (
                <div key={i} className="text-xs border-l-2 border-gray-200 pl-3 py-1 hover:bg-gray-50 rounded-r">
                  <div className="flex justify-between text-gray-400 mb-0.5 font-mono text-[10px]">
                    <span>{log.agent}</span>
                    <span>{log.time}</span>
                  </div>
                  <div className="text-gray-700 font-medium leading-relaxed">{log.msg}</div>
                </div>
              ))}
            </div>
          </div>
        </aside>

        {/* RIGHT COLUMN: Content */}
        <RfpList 
          rfps={rfps} 
          filterStatus={filterStatus} 
          setFilterStatus={setFilterStatus} 
          searchTerm={searchTerm} 
          setSearchTerm={setSearchTerm} 
        />
      </div>
    </div>
  );
}