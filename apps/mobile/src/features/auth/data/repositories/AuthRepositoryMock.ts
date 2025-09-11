import type { AuthRepository } from '../../domain/repositories/AuthRepository';
import type { User } from '../../domain/entities/User';
import { Email } from '../../domain/value-objects/Email';
import { Password } from '../../domain/value-objects/Password';

export class AuthRepositoryMock implements AuthRepository {
    async login({
        email,
        password,
    }: {
        email: Email;
        password: Password;
    }): Promise<{ user: User }> {
        await new Promise((r) => setTimeout(r, 600));
        if (password.toString() !== '123456')
            throw new Error('Credenciales inválidas');
        return {
            user: {
                id: '1',
                name: 'Demo',
                email: email.toString(),
                token: 'fake',
                phone: 234234234,
            },
        };
    }
    async register({
        name,
        phone,
        email,
        password,
    }: {
        name: string;
        phone: number;
        email: Email;
        password: Password;
    }): Promise<{ user: User }> {
        await new Promise((r) => setTimeout(r, 600));
        return {
            user: {
                id: '1',
                name: 'Demo',
                email: email.toString(),
                token: 'fake',
                phone: phone,
            },
        };
    }
    async logout(): Promise<void> {
        await new Promise((r) => setTimeout(r, 600));
    }
    async refreshToken(token: string): Promise<{ user: User }> {
        await new Promise((r) => setTimeout(r, 600));
        return {
            user: {
                id: '1',
                name: 'Demo',
                email: Email.toString(),
                token: 'fake',
                phone: 234234234,
            },
        };
    }
    async recoverPassword(email: Email): Promise<void> {
        await new Promise((r) => setTimeout(r, 600));
    }
}
