import { useAuthStore } from '../../store/authStore';
import { useNavigate, Link } from 'react-router-dom';

export function UserLayout({ children }) {
  const { user, clearAuth } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    clearAuth();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-brand-cream font-lato">
      <header className="bg-brand-teal text-white shadow-lg">
        <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full border-2 border-brand-gold flex items-center justify-center bg-white/10 overflow-hidden">
               <span className="text-brand-gold font-playfair font-bold text-xl">A</span>
            </div>
            <h1 className="font-playfair font-bold text-xl md:text-2xl tracking-wide">رحلة البزنس المرتب</h1>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="text-right hidden sm:block">
              <p className="text-xs text-brand-gold-pale/70 uppercase tracking-tighter">Learner</p>
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
