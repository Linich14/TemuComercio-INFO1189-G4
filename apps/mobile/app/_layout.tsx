import '../global.css';

import { Slot, useSegments, useRouter } from 'expo-router';
import { useCallback, useEffect, useState } from 'react';
import { View, ActivityIndicator, Text } from 'react-native';
import {
    AuthProvider,
    useAuth,
} from '~/src/features/auth/presentation/providers/AuthProvider';

function AuthRoot() {
    const { isAuthenticated, isLoading } = useAuth();
    const segments = useSegments();
    const router = useRouter();

    const handleNavigation = useCallback(() => {
        const inAuthGroup = segments[0] === '(auth)';

        if (isLoading) {
            // Mientras se carga el estado de autenticación, no hacer nada
            return;
        }

        if (!isAuthenticated && !inAuthGroup) {
            // Usuario no autenticado y no está en una ruta de autenticación
            router.replace('/(auth)');
        } else if (isAuthenticated && inAuthGroup) {
            // Usuario autenticado y está en una ruta de autenticación
            router.replace('/(app)');
        }
    }, [isAuthenticated, isLoading, segments, router]);

    useEffect(() => {
        handleNavigation();
    }, [handleNavigation]);

    return (
        <>
            <Slot
                screenOptions={{
                    headerShown: false,
                }}
            />
        </>
    );
}

export default function Layout() {
    return (
        <AuthProvider>
            <AuthRoot />
        </AuthProvider>
    );
}
