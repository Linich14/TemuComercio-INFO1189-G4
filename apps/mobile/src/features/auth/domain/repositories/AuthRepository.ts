import type { User } from '../entities/User';
import { Email } from '../value-objects/Email';
import { Password } from '../value-objects/Password';

export interface AuthRepository {
    login(params: {
        email: Email;
        password: Password;
    }): Promise<{ user: User }>;
    register(params: {
        name: string;
        phone: number;
        email: Email;
        password: Password;
    }): Promise<{ user: User }>;
    logout(): Promise<void>;
    refreshToken(token: string): Promise<{ user: User }>;
    recoverPassword(email: Email): Promise<void>;
}
