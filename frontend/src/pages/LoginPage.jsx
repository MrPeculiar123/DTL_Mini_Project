import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Bot, Lock, ArrowRight } from "lucide-react";

export default function LoginPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleLogin = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      navigate("/dashboard");
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-2xl overflow-hidden">
        <div className="p-8">
          <div className="flex justify-center mb-6">
            <div className="h-12 w-12 bg-blue-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-blue-200">
              <Bot size={28} />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-center text-gray-800 mb-2">Welcome Back</h2>
          <p className="text-center text-gray-500 mb-8">Sign in to NexusBot RFP Manager</p>

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
              <input 
                type="email" 
                defaultValue="admin@synergia.com"
                className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <div className="relative">
                <input 
                  type="password" 
                  defaultValue="password123"
                  className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all"
                />
                <Lock className="absolute right-3 top-3.5 text-gray-400" size={18} />
              </div>
            </div>
            
            <button 
              type="submit" 
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg shadow-lg shadow-blue-900/20 transition-all flex items-center justify-center gap-2 group"
            >
              {loading ? "Signing in..." : "Sign In"}
              {!loading && <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />}
            </button>
          </form>
        </div>
        <div className="bg-gray-50 px-8 py-4 border-t border-gray-100 text-center text-xs text-gray-400">
          Protected by Enterprise Grade Security
        </div>
      </div>
    </div>
  );
}