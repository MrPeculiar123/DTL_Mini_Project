import { Activity, FileText, CheckCircle, XCircle } from "lucide-react";

function StatRow({ label, value, icon }) {
  return (
    <div className="flex items-center justify-between p-2 hover:bg-gray-50 rounded-lg transition-colors">
      <div className="flex items-center gap-3">
        <div className="p-1.5 bg-gray-50 rounded-md">{icon}</div>
        <span className="text-sm text-gray-600 font-medium">{label}</span>
      </div>
      <span className="text-lg font-bold text-gray-900">{value}</span>
    </div>
  );
}

export default function StatsCard({ rfps }) {
  const activeCount = rfps.length;
  const qualifiedCount = rfps.filter(r => r.status === 'QUALIFIED' || r.status === 'COMPLETED').length;
  const rejectedCount = rfps.filter(r => r.status === 'REJECTED').length;

  return (
    <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-200">
      <h3 className="text-xs font-bold text-gray-400 uppercase mb-4 flex items-center gap-2">
        <Activity size={14} /> Pipeline Stats
      </h3>
      <div className="space-y-4">
        <StatRow label="Active RFPs" value={activeCount} icon={<FileText size={16} className="text-blue-500" />} />
        <StatRow label="Qualified" value={qualifiedCount} icon={<CheckCircle size={16} className="text-green-500" />} />
        <StatRow label="Rejected" value={rejectedCount} icon={<XCircle size={16} className="text-red-500" />} />
      </div>
    </div>
  );
}