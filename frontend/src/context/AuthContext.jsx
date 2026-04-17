import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem('access_token') || null);
    const [loading, setLoading] = useState(true);

    const api = axios.create({
        baseURL: 'http://localhost:8000/api',
    });

    api.interceptors.request.use((config) => {
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    });

    useEffect(() => {
        if (token) {
            localStorage.setItem('access_token', token);
            fetchUser();
        } else {
            localStorage.removeItem('access_token');
            setUser(null);
            setLoading(false);
        }
    }, [token]);

    const fetchUser = async () => {
        try {
            const res = await api.get('/auth/me');
            setUser(res.data);
        } catch (error) {
            console.error('Session expired or invalid');
            setToken(null);
        } finally {
            setLoading(false);
        }
    };

    const login = async (username, password) => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        
        try {
            const res = await api.post('/auth/login', formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });
            setToken(res.data.access_token);
            return { success: true };
        } catch (error) {
            return { success: false, message: error.response?.data?.detail || "Login failed" };
        }
    };

    const register = async (email, password) => {
        try {
            await api.post('/auth/register', { email, password });
            return { success: true };
        } catch (error) {
            return { success: false, message: error.response?.data?.detail || "Registration failed" };
        }
    };

    const verifyOtp = async (email, otp_code) => {
        try {
            await api.post('/auth/verify-otp', { email, otp_code });
            return { success: true };
        } catch (error) {
            return { success: false, message: error.response?.data?.detail || "Verification failed" };
        }
    };

    const logout = () => {
        setToken(null);
    };

    const value = { user, token, api, login, register, verifyOtp, logout, loading };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
};
