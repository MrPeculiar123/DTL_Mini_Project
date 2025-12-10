import { Search, Globe, Activity, ExternalLink, Download, ChevronRight } from "lucide-react";
import { getDownloadUrl } from "../services/rfpApi";

export default function RfpList({ rfps, filterStatus, setFilterStatus, searchTerm, setSearchTerm }) {
  
  const getStatusStyle = (status) => {
    switch (status) {
      case "NEW": return "bg-blue-50 text-blue-700 border-blue-200";
      case "QUALIFIED": return "bg-green-50 text-green-700 border-green-200";
      case "PROCESSING": return "bg-purple-50 text-purple-700 border-purple-200";
      case "REJECTED": return "bg-red-50 text-red-700 border-red-200";
      case "COMPLETED": return "bg-orange-50 text-orange-800 border-orange-200";
      default: return "bg-gray-50 text-gray-600 border-gray-200";
    }
  };

  return (
    <div className="col-span-12 md:col-span-9">
      {/* Filter Bar */}
      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 mb-6 flex flex-wrap gap-4 items-center justify-between">
        <div className="flex gap-3">
            <select 
              className="bg-gray-50 border border-gray-300 text-gray-700 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 outline-none"
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
            >
              <option value="ALL">All Statuses</option>
              <option value="NEW">New</option>
              <option value="QUALIFIED">Qualified</option>
              <option value="PROCESSING">Processing</option>
              <option value="COMPLETED">Completed</option>
              <option value="REJECTED">Rejected</option>
            </select>
        </div>
        <div className="relative w-full md:w-64">
          <Search size={16} className="absolute left-3 top-3 text-gray-400" />
          <input 
            type="text" 
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5 outline-none transition-all focus:bg-white" 
            placeholder="Search RFPs..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-lg font-bold text-gray-800">RFP Pipeline</h2>
          <span className="text-xs font-medium text-gray-400 bg-gray-100 px-2 py-1 rounded-full">{rfps.length} items</span>
        </div>
        
        {rfps.length === 0 ? (
          <div className="bg-white p-12 rounded-xl border border-dashed border-gray-300 text-center flex flex-col items-center justify-center text-gray-500">
            <Search size={48} className="text-gray-200 mb-4" />
            <p>No RFPs found matching your criteria.</p>
          </div>
        ) : (
          rfps.map((r) => (
            <div key={r.id} className="group bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md hover:border-blue-200 transition-all flex flex-col md:flex-row justify-between gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-xs font-mono text-gray-400 bg-gray-50 px-1.5 rounded">#{r.id}</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded border tracking-wide ${getStatusStyle(r.status)}`}>
                    {r.status}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">{r.title}</h3>
                <div className="text-sm text-gray-500 flex flex-wrap gap-x-6 gap-y-2">
                  <span className="flex items-center gap-1.5"><Activity size={14} className="text-gray-400"/> Due: <span className="font-medium text-gray-700">{r.due_date}</span></span>
                  <span className="flex items-center gap-1.5"><Globe size={14} className="text-gray-400"/> Portal: <span className="font-medium text-gray-700">{r.portal}</span></span>
                </div>
              </div>

              <div className="flex flex-row md:flex-col gap-2 justify-center border-t md:border-t-0 md:border-l border-gray-50 pt-4 md:pt-0 md:pl-6 min-w-[150px]">
                <button className="text-sm text-gray-600 font-medium hover:text-blue-600 text-left flex items-center gap-2 group/btn">
                  View Details <ExternalLink size={14} className="opacity-0 group-hover/btn:opacity-100 transition-opacity" />
                </button>
                {r.filename ? (
                   <a href={getDownloadUrl(r.id)} target="_blank" rel="noopener noreferrer" className="text-sm text-gray-600 font-medium hover:text-blue-600 text-left flex items-center gap-2 mt-1">
                     Download PDF <Download size={14} />
                   </a>
                ) : (
                  <span className="text-sm text-gray-300 cursor-not-allowed flex items-center gap-2">No Document</span>
                )}
                {r.status === 'NEW' && (
                   <button className="mt-3 text-xs bg-blue-50 text-blue-600 px-3 py-2 rounded-lg hover:bg-blue-100 font-bold flex items-center justify-center gap-1 transition-colors">
                     Analyze Now <ChevronRight size={12} />
                   </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}