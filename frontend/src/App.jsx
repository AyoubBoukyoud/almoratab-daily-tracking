import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import Login from './pages/Login';
import UserDashboard from './pages/UserDashboard';
import AdminPanel from './pages/admin/AdminPanel';
import UserDetail from './pages/admin/UserDetail';

export default function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-center" reverseOrder={false} />
      <Routes>
        <Route path="/login" element={<Login />} />
        
        {/* User Routes */}
        <Route path="/dashboard" element={
          <ProtectedRoute requiredRole={["user", "superUser"]}>
            <UserDashboard />
          </ProtectedRoute>
        } />
        
        {/* Admin Routes */}
        <Route path="/admin" element={
          <ProtectedRoute requiredRole={["admin", "superUser"]}>
            <AdminPanel />
          </ProtectedRoute>
        } />
        <Route path="/admin/users/:userId" element={
          <ProtectedRoute requiredRole={["admin", "superUser"]}>
            <UserDetail />
          </ProtectedRoute>
        } />

        {/* Catch-all */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
