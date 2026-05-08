import { createContext, useState, useEffect } from 'react';
import api from '../services/api';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedUser = localStorage.getItem('@App:user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  async function login(email, password) {
    try {

      const response = await api.post('/auth/login', { email, password });
      const data = response.data;

      setUser(data);
      localStorage.setItem('@App:user', JSON.stringify(data));

      return data;
    } catch (error) {
      const message = error.response?.data?.error ?? 'Erro ao fazer login';
      throw new Error(message);
    }
  }

  function logout() {
    setUser(null);
    localStorage.removeItem('@App:user');
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}