import { Bot, User, LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom"; // Import this

export default function Navbar({ user }) {
  const navigate = useNavigate(); // Hook for navigation

  const handleLogout = () => {
    // In a real app, clear tokens here
    navigate("/login");
  };

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-3 flex justify-between items-center sticky top-0 z-20 shadow-sm">
      <div className="flex items-center gap-3 cursor-pointer" onClick={() => navigate("/dashboard")}>
        <div className="h-9 w-9 bg-blue-600 rounded-lg flex items-center justify-center text-white shadow-lg shadow-blue-200">
          <Bot size={20} />
        </div>
        <span className="font-bold text-xl tracking-tight text-gray-900">
          NexusBot <span className="text-gray-400 font-normal text-base">| RFP Manager</span>
        </span>
      </div>
      
      <div className="flex items-center gap-6">
        <div className="text-right hidden sm:block">
          <div className="text-sm font-bold text-gray-900">{user.username}</div>
          <div className="text-xs text-gray-500">{user.role}</div>
        </div>
        
        <div className="flex items-center gap-3 pl-6 border-l border-gray-100">
          {user.avatar ? (
            <img src={user.avatar} alt="Profile" className="h-9 w-9 rounded-full border border-gray-200" />
          ) : (
            <div className="h-9 w-9 rounded-full bg-gray-100 flex items-center justify-center text-gray-400">
              <User size={18} />
            </div>
          )}
          
          <button 
            onClick={handleLogout} // Attach handler
            className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors" 
            title="Logout"
          >
            <LogOut size={20} />
          </button>
        </div>
      </div>
    </nav>
  );
}