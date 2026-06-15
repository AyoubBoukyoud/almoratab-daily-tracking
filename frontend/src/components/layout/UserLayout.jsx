import { useAuthStore } from '../../store/authStore';
import { useNavigate, Link } from 'react-router-dom';
import logo from '../../assets/logo.png';

export function UserLayout({ children }) {
  const { user, role, clearAuth } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    clearAuth();
    navigate('/login');
  };

  const today = new Date().toLocaleDateString('fr-FR', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });

  const canAccessAdmin = role === 'admin' || role === 'superUser';

  return (
    <div className="min-h-screen bg-brand-cream font-lato">
      <header className="bg-brand-teal text-white shadow-lg">
        <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Link to="/dashboard" className="flex items-center gap-3 group">
              <div className="w-10 h-10 rounded-full border-2 border-brand-gold flex items-center justify-center bg-white overflow-hidden transition-transform group-hover:scale-110">
                 <img src={logo} alt="Logo" className="w-8 h-8 object-contain" />
              </div>
              <div>
                <h1 className="font-playfair font-bold text-xl md:text-2xl tracking-wide">رحلة البزنس المرتب</h1>
                <p className="text-[10px] text-brand-gold-pale/60 font-medium uppercase tracking-widest">{today}</p>
              </div>
            </Link>
          </div>
          
          <div className="flex items-center gap-4">
            {canAccessAdmin && (
              <Link 
                to="/admin"
                className="hidden md:flex items-center gap-1 px-3 py-1 bg-brand-gold text-brand-dark rounded-md text-xs font-black uppercase transition-transform hover:scale-105"
              >
                <span>⚙️</span> Admin Panel
              </Link>
            )}
            <div className="text-right hidden sm:block">
              <p className="text-xs text-brand-gold-pale/70 uppercase tracking-tighter">
                {role === 'superUser' ? 'Super User' : 'Learner'}
              </p>
              <p className="text-sm font-bold">Bonjour, {user?.full_name?.split(' ')[0] || 'User'} 👋</p>
            </div>
            <button 
              onClick={handleLogout}
              className="p-2 hover:bg-white/10 rounded-full transition-colors"
              title="Logout"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {children}
      </main>

      <footer className="max-w-4xl mx-auto px-4 py-8 text-center text-brand-muted text-xs">
        <p>© 2026 رحلة البزنس المرتب · Created with Excellence</p>
      </footer>
    </div>
  );
}
