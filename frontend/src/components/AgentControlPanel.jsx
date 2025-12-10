import { Cpu, Globe, Filter, Loader2 } from "lucide-react";

function AgentButton({ label, onClick, loading, icon, step }) {
  return (
    <button
      onClick={onClick}
      disabled={loading}
      className={`w-full flex items-center justify-between px-4 py-3 rounded-lg font-medium transition-all group ${
        loading ? "bg-slate-800 cursor-wait border border-slate-700" : "bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-900/20"
      }`}
    >
      <div className="flex items-center gap-3">
        <span className={`flex items-center justify-center w-5 h-5 rounded text-[10px] font-bold ${loading ? 'bg-slate-700 text-slate-400' : 'bg-blue-700 text-blue-100'}`}>
          {step}
        </span>
        <div className="flex items-center gap-2">
          <span className={`${loading ? 'text-slate-500' : 'text-blue-200'}`}>{loading ? <Loader2 size={16} className="animate-spin"/> : icon}</span>
          <span className={loading ? 'text-slate-400' : 'text-white'}>{loading ? "Processing..." : label}</span>
        </div>
      </div>
    </button>
  );
}

export default function AgentControlPanel({ actionLoading, onAction }) {
  return (
    <div className="bg-slate-900 p-5 rounded-xl shadow-lg text-white">
      <h3 className="text-xs font-bold text-slate-400 uppercase mb-4 flex items-center gap-2">
        <Cpu size={14} /> Agent Controls
      </h3>
      <div className="space-y-3">
        <AgentButton 
          label="Run Scraper" 
          loading={actionLoading === "scraper"} 
          onClick={() => onAction("scraper")}
          icon={<Globe size={16} />}
          step="1"
        />
        <AgentButton 
          label="Filter RFPs" 
          loading={actionLoading === "sales"} 
          onClick={() => onAction("sales")}
          icon={<Filter size={16} />}
          step="2"
        />
        <AgentButton 
          label="Auto-Assign" 
          loading={actionLoading === "main"} 
          onClick={() => onAction("main")}
          icon={<Cpu size={16} />}
          step="3"
        />
      </div>
    </div>
  );
}