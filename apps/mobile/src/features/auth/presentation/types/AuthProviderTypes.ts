import { User } from '../../domain/entities/User';
import { Session } from '../../domain/entities/Session';

export interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    error: string | null;
}

export interface AuthContextType extends AuthState {
    login: (email: string, password: string) => Promise<void>;
    register: (
        email: string,
        password: string,
        name: string,
        lastName: string,
        rut: string,
        phone?: number
    ) => Promise<void>;
    logout: () => Promise<void>;
    recoverPassword: (email: string) => Promise<void>;
}
