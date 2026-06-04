import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

export function ProtectedRoute({ children, requiredRole }) {
  const { token, role, isHydrated } = useAuthStore();

  if (!isHydrated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-brand-cream">
        <div className="w-10 h-10 border-4 border-brand-gold border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (requiredRole && role !== requiredRole) {
    // If admin is trying to access user page or vice versa
    if (role === 'admin') {
      return <Navigate to="/admin" replace />;
    }
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}
export default ProtectedRoute;
