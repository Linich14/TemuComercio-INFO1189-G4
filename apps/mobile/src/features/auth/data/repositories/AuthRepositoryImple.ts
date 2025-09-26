import type { AuthRepository } from '../../domain/repositories/AuthRepository';
import { Email } from '../../domain/value-objects/Email';
import { Rut } from '../../domain/value-objects/Rut';
import { Password } from '../../domain/value-objects/Password';
import { User } from '../../domain/entities/User';
import { api } from '../../../../shared/infra/http/api';
import { toDomainUser } from '../mappers/UserMapper';
import { SessionMapper } from '../mappers/SessionMapper';
import type { SessionDTO } from '../models/SessionDTO';
import type { TokenStorage } from '../../domain/ports/TokenStorage';
import type { UserStorage } from '../../domain/ports/UserStorage';

export class AuthRepositoryImpl implements AuthRepository {
    constructor(
        private tokenStorage: TokenStorage,
        private userStorage: UserStorage
    ) {}

    async login(params: { email: Email; password: Password }): Promise<User> {
        try {
            console.log('Login attempt with:', {
                email: params.email.toString(),
                password: '***hidden***',
            });

            const response = await api.post<SessionDTO>('/auth/login/', {
                email: params.email.toString(),
                password: params.password.toString(),
            });

            console.log('Login response:', response.data);

            const session = SessionMapper.toDomain(response.data);

            // Guardar token y usuario
            console.log('Saving session data:', session);
            await this.tokenStorage.saveToken(session.accessToken);
            await this.userStorage.saveUser(session.user);

            return session.user;
        } catch (error: any) {
            console.error('Login error details:', {
                status: error.response?.status,
                data: error.response?.data,
                message: error.message,
            });

            // Manejo específico de errores
            if (error.response?.status === 401) {
                throw new Error('Credenciales inválidas');
            } else if (error.response?.status === 404) {
                throw new Error('Usuario no encontrado');
            } else if (error.response?.status === 400) {
                const message =
                    error.response?.data?.message || 'Datos inválidos';
                throw new Error(message);
            } else if (error.response?.status >= 500) {
                throw new Error('Error del servidor. Intenta más tarde');
            } else if (error.code === 'NETWORK_ERROR' || !error.response) {
                throw new Error('Error de conexión. Verifica tu internet');
            }

            throw new Error(
                error.response?.data?.message || 'Error al iniciar sesión'
            );
        }
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
        try {
            const response = await api.post<SessionDTO>('/auth/register/', {
                name: params.name,
                lastName: params.lastName,
                phone: params.phone,
                email: params.email.toString(),
                run: params.run,
                rut: params.rut.getValue(),
                password: params.password.toString(),
            });

            const { user, accessToken, refreshToken } = SessionMapper.toDomain(
                response.data
            );

            await this.tokenStorage.saveToken(accessToken);
            if (refreshToken) {
                // Guardar refresh token si es necesario
            }

            const domainUser = toDomainUser(user);
            await this.userStorage.saveUser(domainUser);

            return domainUser;
        } catch (error: any) {
            if (error.response?.status === 409) {
                throw new Error('El usuario ya existe');
            } else if (error.response?.status === 400) {
                throw new Error('Datos inválidos');
            }

            throw new Error(
                error.response?.data?.message || 'Error al registrar usuario'
            );
        }
    }

    async logout(): Promise<void> {
        try {
            const token = await this.tokenStorage.getToken();

            if (token) {
                // Opcional: llamar al endpoint de logout en el servidor
                try {
                    await api.post(
                        '/auth/logout/',
                        {},
                        {
                            headers: {
                                Authorization: `Bearer ${token}`,
                            },
                        }
                    );
                } catch {
                    // Si falla el logout en el servidor, continuamos con el logout local
                }
            }

            // Limpiar storage local
            await this.tokenStorage.deleteToken();
            await this.userStorage.deleteUser();
        } catch (error) {
            // En caso de error, aseguramos que se limpie el storage local
            await this.tokenStorage.deleteToken();
            await this.userStorage.deleteUser();
            throw new Error('Error al cerrar sesión');
        }
    }

    async refreshToken(token: string): Promise<User> {
        try {
            const response = await api.post<SessionDTO>('/auth/refresh/', {
                refreshToken: token,
            });

            const {
                user,
                accessToken,
                refreshToken: newRefreshToken,
            } = response.data;

            await this.tokenStorage.saveToken(accessToken);
            if (newRefreshToken) {
                // Actualizar refresh token
            }

            const domainUser = toDomainUser(user);
            await this.userStorage.saveUser(domainUser);

            return domainUser;
        } catch (error: any) {
            // Si falla el refresh, limpiar storage
            await this.tokenStorage.deleteToken();
            await this.userStorage.deleteUser();

            throw new Error('Sesión expirada. Inicia sesión nuevamente');
        }
    }

    async recoverPassword(email: Email): Promise<void> {
        try {
            await api.post('/auth/recover-password/', {
                email: email.toString(),
            });
        } catch (error: any) {
            if (error.response?.status === 404) {
                throw new Error('Email no registrado');
            }

            throw new Error(
                error.response?.data?.message ||
                    'Error al enviar email de recuperación'
            );
        }
    }

    async isAuthenticated(): Promise<boolean> {
        try {
            const token = await this.tokenStorage.getToken();
            const user = await this.userStorage.getUser();

            if (!token || !user) {
                return false;
            }

            // Opcional: verificar token en el servidor
            try {
                await api.get('/auth/profile/', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                return true;
            } catch {
                // Token inválido, limpiar storage
                await this.tokenStorage.deleteToken();
                await this.userStorage.deleteUser();
                return false;
            }
        } catch {
            return false;
        }
    }

    async getCurrentUser(): Promise<User | null> {
        try {
            const user = await this.userStorage.getUser();
            return user;
        } catch {
            return null;
        }
    }
}
