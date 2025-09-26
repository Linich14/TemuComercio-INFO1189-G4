import React, {
    createContext,
    useContext,
    useState,
    useEffect,
    use,
} from 'react';
import authContainer from '../../infra/di/AuthContainer';
import { AuthContextType, AuthState } from '../types/AuthProviderTypes';
import { Email } from '../../domain/value-objects/Email';
import { Password } from '../../domain/value-objects/Password';
import { Rut } from '../../domain/value-objects/Rut';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
    children,
}) => {
    const [state, setState] = useState<AuthState>({
        user: null,
        isAuthenticated: false,
        isLoading: true,
        error: null,
    });

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const isAuthenticated = await authContainer.getAuthUseCase();

                if (isAuthenticated) {
                    const user = await authContainer.getCurrentUserUseCase();
                    setState({
                        user,
                        isLoading: false,
                        isAuthenticated: true,
                        error: null,
                    });
                } else {
                    setState({
                        user: null,
                        isLoading: false,
                        isAuthenticated: false,
                        error: null,
                    });
                }
            } catch (err) {
                setState({
                    user: null,
                    isLoading: false,
                    isAuthenticated: false,
                    error: 'Error al restaurar sesión',
                });
            }
        };

        checkAuth();
    }, []);

    const login = async (email: string, password: string): Promise<void> => {
        try {
            setState((prev) => ({ ...prev, isLoading: true, error: null }));
            const user = await authContainer.getLoginUseCase().execute({
                email: Email.create(email),
                password: Password.create(password),
            });

            setState({
                user,
                isLoading: false,
                isAuthenticated: true,
                error: null,
            });
        } catch (error) {
            setState({
                ...state,
                isLoading: false,
                error:
                    error instanceof Error
                        ? error.message
                        : 'Error al iniciar sesiónsdfgsdf',
            });
            throw error;
        }
    };

    const logout = async (): Promise<void> => {
        try {
            setState((prev) => ({ ...prev, isLoading: true, error: null }));
            await authContainer.getLogoutUseCase().execute();
            setState({
                user: null,
                isLoading: false,
                isAuthenticated: false,
                error: null,
            });
        } catch (error) {
            setState({
                ...state,
                isLoading: false,
                error:
                    error instanceof Error
                        ? error.message
                        : 'Error al cerrar sesión',
            });
            throw error;
        }
    };

    const register = async (
        email: string,
        password: string,
        name: string,
        lastName: string,
        rut: string,
        phone?: number
    ): Promise<void> => {
        try {
            setState((prev) => ({ ...prev, isLoading: true, error: null }));
            const user = await authContainer.getRegisterUseCase().execute({
                email: Email.create(email),
                password: Password.create(password),
                name,
                lastName,
                rut: Rut.create(rut),
                phone,
            });
            setState({
                user: user,
                isLoading: false,
                isAuthenticated: true,
                error: null,
            });
        } catch (error) {
            setState({
                ...state,
                isLoading: false,
                error:
                    error instanceof Error
                        ? error.message
                        : 'Error al cerrar sesión',
            });
            throw error;
        }
    };

    const recoverPassword = async (email: string): Promise<void> => {
        try {
            setState((prev) => ({ ...prev, isLoading: true, error: null }));
            await authContainer
                .getRecoverPasswordUseCase()
                .execute({ email: Email.create(email) });
            setState((prev) => ({ ...prev, isLoading: false }));
        } catch (error) {
            setState({
                ...state,
                isLoading: false,
                error:
                    error instanceof Error
                        ? error.message
                        : 'Error al cerrar sesión',
            });
            throw error;
        }
    };

    return (
        <AuthContext.Provider
            value={{
                ...state,
                login,
                logout,
                register,
                recoverPassword,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = (): AuthContextType => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth debe usarse dentro de un AuthProvider');
    }
    return context;
};

export default AuthProvider;
