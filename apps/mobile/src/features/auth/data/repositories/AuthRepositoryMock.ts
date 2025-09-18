import type { AuthRepository } from '../../domain/repositories/AuthRepository';
import type { Session } from '../../domain/entities/Session';
import { Email } from '../../domain/value-objects/Email';
import { Password } from '../../domain/value-objects/Password';
import { Rut } from '../../domain/value-objects/Rut';
import { TokenStorage } from '../../domain/ports/TokenStorage';
import { UserStorage } from '../../domain/ports/UserStorage';
import { User } from '../../domain/entities/User';

const MOCK_USER: User = {
    id: '1',
    name: 'Demo',
    lastName: 'User',
    email: Email.create('axe@gmail.com'),
    rut: Rut.create('12345678-9'),
};

export class AuthRepositoryMock implements AuthRepository {
    constructor(
        private tokenStorage: TokenStorage,
        private userStorage: UserStorage
    ) {}

    async login(params: { email: Email; password: Password }): Promise<User> {
        await new Promise((r) => setTimeout(r, 600));

        if (params.password.toString() !== '123456')
            throw new Error('Credenciales inválidas');

        await this.tokenStorage.saveToken('mock-token');
        await this.userStorage.saveUser(MOCK_USER);
        return MOCK_USER;
    }

    async register(params: {
        name: string;
        lastName: string;
        phone?: number;
        email: Email;
        run?: string;
        rut: Rut;
        password: Password;
    }): Promise<User> {
        await new Promise((r) => setTimeout(r, 600));
        await this.tokenStorage.saveToken('mock-token');
        await this.userStorage.saveUser(MOCK_USER);
        return MOCK_USER;
    }

    async logout(): Promise<void> {
        await new Promise((r) => setTimeout(r, 600));
        await this.tokenStorage.deleteToken();
        await this.userStorage.deleteUser();
    }
    async refreshToken(token: string): Promise<User> {
        await new Promise((r) => setTimeout(r, 600));
        return MOCK_USER;
    }
    async recoverPassword(email: Email): Promise<void> {
        await new Promise((r) => setTimeout(r, 600));
    }

    async isAuthenticated(): Promise<boolean> {
        const token = await this.tokenStorage.getToken();
        const user = await this.userStorage.getUser();
        return !!token && !!user;
    }

    async getCurrentUser(): Promise<User | null> {
        const user = await this.userStorage.getUser();
        return user;
    }
}
