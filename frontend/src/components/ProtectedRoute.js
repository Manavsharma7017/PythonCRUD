import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { authAPI } from '../api/api';

function ProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setIsAuthenticated(false);
        setLoading(false);
        return;
      }

      try {
        await authAPI.getCurrentUser();
        setIsAuthenticated(true);
      } catch (error) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
}

export default ProtectedRoute;
