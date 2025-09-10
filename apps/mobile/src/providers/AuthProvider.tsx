// src/providers/AuthProvider.tsx
import React, {
    createContext,
    useContext,
    useMemo,
    useState,
    useEffect,
} from 'react';
import { useRouter, useSegments } from 'expo-router';
import type { User } from '~/src/features/auth/domain/entities/User';
import { View, ActivityIndicator, Text } from 'react-native';

type Ctx = {
    user: User | null;
    isLoading: boolean;
    signIn: (user: User) => void;
    signOut: () => void;
};

const AuthContext = createContext<Ctx | null>(null);

export const AuthProvider: React.FC<React.PropsWithChildren> = ({
    children,
}) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const segments = useSegments();
    const router = useRouter();

    const signIn = useMemo(
        () => (user: User) => {
            setUser(user);
            // Redirigir a la app después del login
            router.replace('/(app)');
        },
        [router]
    );

    const signOut = useMemo(
        () => () => {
            setUser(null);
            // Redirigir al login después del logout
            router.replace('/(auth)');
        },
        [router]
    );

    const contextValue = useMemo(
        () => ({
            user,
            isLoading,
            signIn,
            signOut,
        }),
        [user, isLoading, signIn, signOut]
    );

    useEffect(() => {
        const initializeAuth = async () => {
            try {
                await new Promise((resolve) => setTimeout(resolve, 1000)); // Simular carga
            } catch (error) {
                console.error('Error initializing auth:', error);
            } finally {
                setIsLoading(false);
            }
        };

        initializeAuth();
    }, []);

    useEffect(() => {
        if (isLoading) return; // No hacer nada mientras carga

        const inAuthGroup = segments[0] === '(auth)';

        if (!user && !inAuthGroup) {
            // Usuario no logueado fuera del grupo auth -> ir a login
            router.replace('/(auth)');
        } else if (user && inAuthGroup) {
            // Usuario logueado en grupo auth -> ir a app
            router.replace('/(app)');
        }
    }, [user, segments, isLoading, router]);

    // Mostrar loading mientras se inicializa
    if (isLoading) {
        return (
            <View className="flex-1 items-center justify-center bg-white">
                <ActivityIndicator size="large" color="#0062BF" />
                <Text className="mt-4 text-lg text-gray-600">Cargando...</Text>
            </View>
        );
    }

    return (
        <AuthContext.Provider value={contextValue}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};
