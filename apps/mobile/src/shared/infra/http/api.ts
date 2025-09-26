import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const TOKEN_KEY = 'authToken';

export const api = axios.create({
    baseURL: process.env.EXPO_PUBLIC_API_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor para agregar token automáticamente
api.interceptors.request.use(
    async (config) => {
        try {
            const token = await SecureStore.getItemAsync(TOKEN_KEY);
            if (
                token &&
                !config.url?.includes('/auth/login') &&
                !config.url?.includes('/auth/register')
            ) {
                config.headers.Authorization = `Bearer ${token}`;
            }
        } catch (error) {
            console.error('Error getting token:', error);
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            // Token expirado o inválido
            try {
                await SecureStore.deleteItemAsync(TOKEN_KEY);
                // Aquí podrías disparar un evento para redirigir al login
            } catch {}
        }
        return Promise.reject(error);
    }
);
