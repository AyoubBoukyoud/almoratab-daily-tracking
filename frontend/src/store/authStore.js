import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      token: null,
      role: null,
      isHydrated: false,
      setAuth: (user, token) => set({ user, token, role: user.role }),
      clearAuth: () => set({ user: null, token: null, role: null }),
      setHydrated: () => set({ isHydrated: true })
    }),
    { 
      name: 'almoratab-auth',
      storage: createJSONStorage(() => localStorage),
      onRehydrateStorage: () => (state) => {
        state.setHydrated();
      }
    }
  )
);
