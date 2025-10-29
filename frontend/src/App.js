import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import '@/App.css';
import { Toaster } from '@/components/ui/sonner';
import { toast } from 'sonner';

// Pages
import LandingPage from '@/pages/LandingPage';
import Dashboard from '@/pages/Dashboard';
import Challenges from '@/pages/Challenges';
import ChallengeDetailNew from '@/pages/ChallengeDetailNew';
import Education from '@/pages/Education';
import Leaderboard from '@/pages/Leaderboard';
import AdminPanelNew from '@/pages/AdminPanelNew';
import Courses from '@/pages/Courses';
import CourseViewer from '@/pages/CourseViewer';
import QuizMode from '@/pages/QuizMode';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

// Auth Context
export const AuthContext = React.createContext();

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchUser = async () => {
    try {
      const response = await axios.get(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUser(response.data);
    } catch (error) {
      console.error('Failed to fetch user:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = (newToken, userData) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
    setUser(userData);
    toast.success('Login berhasil! Selamat datang di Tegalsec Lab.');
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    toast.info('Anda telah logout.');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0a0a0b]">
        <div className="text-emerald-400 text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout, refreshUser: fetchUser }}>
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={!user ? <LandingPage /> : <Navigate to="/dashboard" />} />
            <Route path="/dashboard" element={user ? <Dashboard /> : <Navigate to="/" />} />
            <Route path="/challenges" element={user ? <Challenges /> : <Navigate to="/" />} />
            <Route path="/challenges/:id" element={user ? <ChallengeDetailNew /> : <Navigate to="/" />} />
            <Route path="/education" element={user ? <Education /> : <Navigate to="/" />} />
            <Route path="/courses" element={user ? <Courses /> : <Navigate to="/" />} />
            <Route path="/courses/:id" element={user ? <CourseViewer /> : <Navigate to="/" />} />
            <Route path="/quiz" element={user ? <QuizMode /> : <Navigate to="/" />} />
            <Route path="/leaderboard" element={user ? <Leaderboard /> : <Navigate to="/" />} />
            <Route path="/admin" element={user?.role === 'admin' ? <AdminPanelNew /> : <Navigate to="/dashboard" />} />
          </Routes>
        </BrowserRouter>
        <Toaster position="top-right" richColors />
      </div>
    </AuthContext.Provider>
  );
}

export default App;