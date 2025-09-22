import { User } from '../entities/User';
import { Email } from '../value-objects/Email';
import { Password } from '../value-objects/Password';
import { Rut } from '../value-objects/Rut';

export interface AuthRepository {
    // Los metodos que van a consumir la Api
    login(params: { email: Email; password: Password }): Promise<User>;
    register(params: {
        name: string;
        lastName: string;
        phone?: number;
        email: Email;
        run?: string;
        rut: Rut;
        password: Password;
    }): Promise<User>;
    logout(): Promise<void>;
    refreshToken(token: string): Promise<User>;
    recoverPassword(email: Email): Promise<void>;
    // Para verificar el usuario autenticado al iniciar la app
    isAuthenticated(): Promise<boolean>;
    getCurrentUser(): Promise<User | null>;
}
