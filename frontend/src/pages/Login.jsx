import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { login } from '../api/auth';
import toast from 'react-hot-toast';
import { Lock, Mail, Loader2, Eye, EyeOff } from 'lucide-react';
import logo from '../assets/logo.png';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      toast.error('الرجاء إدخال البريد الإلكتروني وكلمة المرور');
      return;
    }

    setIsLoading(true);
    try {
      const data = await login(email, password);
      setAuth(data.user, data.access_token);
      toast.success(`مرحباً بك، ${data.user.full_name}! 👋`);
      
      if (data.user.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/dashboard');
      }
    } catch (error) {
      console.error(error);
      const detail = error.response?.data?.detail;
      toast.error(detail || 'فشل تسجيل الدخول. يرجى التحقق من البيانات.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-tr from-brand-dark via-brand-teal to-brand-teal-mid p-4 relative overflow-hidden">
      {/* Background blobs for premium depth */}
      <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-brand-gold opacity-10 blur-[100px] rounded-full pointer-events-none"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-brand-teal-light opacity-20 blur-[120px] rounded-full pointer-events-none"></div>

      <div className="w-full max-w-md bg-white/5 backdrop-blur-xl border border-white/10 p-8 rounded-3xl shadow-2xl relative z-10 transition-all duration-300 hover:shadow-brand-gold/5 hover:border-white/20">
        
        {/* Branding & Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-brand-gold to-brand-gold-light p-0.5 shadow-lg shadow-brand-gold/20 mb-4">
            <div className="w-full h-full bg-white rounded-[14px] flex items-center justify-center p-2">
              <img src={logo} alt="Logo" className="w-full h-full object-contain" />
            </div>
          </div>
          <h1 className="font-playfair text-brand-gold text-3xl font-bold tracking-wide">
            رحلة البزنس المرتب
          </h1>
          <p className="font-cairo text-brand-muted text-sm mt-2">
            منصة تتبع أداءCohort وجمع النقاط
          </p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          
          {/* Email field */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-brand-gold-pale font-cairo text-right">
              البريد الإلكتروني
            </label>
            <div className="relative">
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="email@almoratab.ma"
                className="w-full bg-brand-dark/40 border border-brand-border/30 rounded-2xl py-3 pl-4 pr-11 text-white placeholder-gray-500 focus:outline-none focus:border-brand-gold focus:ring-2 focus:ring-brand-gold/20 transition-all text-left"
              />
              <Mail className="absolute right-4 top-3.5 h-5 w-5 text-brand-muted" />
            </div>
          </div>

          {/* Password field */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-brand-gold-pale font-cairo text-right">
              كلمة المرور
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-brand-dark/40 border border-brand-border/30 rounded-2xl py-3 pl-12 pr-11 text-white placeholder-gray-500 focus:outline-none focus:border-brand-gold focus:ring-2 focus:ring-brand-gold/20 transition-all text-left"
              />
              <Lock className="absolute right-4 top-3.5 h-5 w-5 text-brand-muted" />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute left-4 top-3.5 text-brand-muted hover:text-brand-gold transition-colors"
              >
                {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
              </button>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-brand-gold to-brand-gold-light text-brand-dark font-cairo font-bold py-3.5 px-4 rounded-2xl shadow-lg shadow-brand-gold/15 hover:shadow-brand-gold/25 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-150 flex items-center justify-center gap-2 group disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <Loader2 className="h-5 w-5 animate-spin text-brand-dark" />
            ) : (
              <span className="group-hover:scale-105 transition-transform">دخول للمنصة</span>
            )}
          </button>

        </form>

        {/* Branding Footer */}
        <div className="text-center mt-8 pt-6 border-t border-white/5">
          <p className="text-xs text-brand-muted font-cairo">
            جميع الحقوق محفوظة للبزنس المرتب © 2026
          </p>
        </div>

      </div>
    </div>
  );
}
