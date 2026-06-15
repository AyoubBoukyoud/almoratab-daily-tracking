import { useAuthStore } from '../../store/authStore';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import logo from '../../assets/logo.png';

export function AdminLayout({ children }) {
  const { user, role, clearAuth } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    clearAuth();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-brand-cream font-lato">
      <header className="bg-brand-dark text-white shadow-lg sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
          <div className="flex items-center gap-6">
            <Link to="/admin" className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full border border-brand-gold flex items-center justify-center bg-white overflow-hidden">
                 <img src={logo} alt="Logo" className="w-6 h-6 object-contain" />
              </div>
              <h1 className="font-playfair font-bold text-lg tracking-wide hidden sm:block">رحلة البزنس المرتب</h1>
            </Link>
            
            <nav className="flex items-center gap-1">
              <Link 
                to="/admin" 
                className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${location.pathname === '/admin' ? 'bg-brand-gold text-brand-dark' : 'hover:bg-white/10'}`}
              >
                Leaderboard
              </Link>
              {/* Future admin links can go here */}
            </nav>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="text-right hidden sm:block">
              <p className="text-[10px] text-brand-gold uppercase tracking-widest font-bold">
                {role === 'superUser' ? 'Super User View' : 'Admin Console'}
              </p>
              <p className="text-sm font-medium">{user?.full_name || 'Administrator'}</p>
            </div>
            <button 
              onClick={handleLogout}
              className="p-2 hover:bg-white/10 rounded-full transition-colors text-gray-300 hover:text-white"
              title="Logout"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        {children}
      </main>

      <footer className="max-w-6xl mx-auto px-4 py-8 text-center text-brand-muted text-xs border-t border-brand-border/20 mt-auto">
        <p>© 2026 رحلة البزنس المرتب · Admin Panel v1.0</p>
      </footer>
    </div>
  );
}
