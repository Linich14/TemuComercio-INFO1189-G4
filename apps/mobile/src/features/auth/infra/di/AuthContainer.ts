import { AuthRepositoryMock } from '../../data/repositories/AuthRepositoryMock';
import { AuthRepository } from '../../domain/repositories/AuthRepository';
import { SecureTokenStorage } from '../secure/SecureTokenStorage';
import { TokenStorage } from '../../domain/ports/TokenStorage';
import { SecureUserStorage } from '../secure/UserStorage';
import { UserStorage } from '../../domain/ports/UserStorage';

// Casos de uso
import { LoginUseCase } from '../../domain/usecases/LoginUseCase';
import { LogoutUseCase } from '../../domain/usecases/LogoutUseCase';
import { RecoverPasswordUseCase } from '../../domain/usecases/RecoverPasswordUseCase';
import { RefreshTokenUseCase } from '../../domain/usecases/RefreshTokenUseCase';
import { RegisterUseCase } from '../../domain/usecases/RegisterUseCase';
import { User } from '../../domain/entities/User';

class AuthContainer {
    // Infraestructura y adaptadores
    private readonly tokenStorage: TokenStorage;
    private readonly userStorage: UserStorage;
    private readonly authRepository: AuthRepository;

    // Mappers

    // Casos de uso
    private readonly loginUseCase: LoginUseCase;
    private readonly logoutUseCase: LogoutUseCase;
    private readonly recoverPasswordUseCase: RecoverPasswordUseCase;
    private readonly refreshTokenUseCase: RefreshTokenUseCase;
    private readonly registerUseCase: RegisterUseCase;

    constructor() {
        // Inicializar implementaciones concretas
        this.tokenStorage = new SecureTokenStorage();
        this.userStorage = new SecureUserStorage();

        // Inicializar repositorios con sus dependencias
        this.authRepository = new AuthRepositoryMock(
            this.tokenStorage,
            this.userStorage
        );

        // Inicializar casos de uso con sus dependencias
        this.loginUseCase = new LoginUseCase(this.authRepository);
        this.logoutUseCase = new LogoutUseCase(this.authRepository);
        this.recoverPasswordUseCase = new RecoverPasswordUseCase(
            this.authRepository
        );
        this.refreshTokenUseCase = new RefreshTokenUseCase(this.authRepository);
        this.registerUseCase = new RegisterUseCase(this.authRepository);
    }

    // Getters para acceder a los casos de uso
    getLoginUseCase(): LoginUseCase {
        return this.loginUseCase;
    }

    getLogoutUseCase(): LogoutUseCase {
        return this.logoutUseCase;
    }

    getRecoverPasswordUseCase(): RecoverPasswordUseCase {
        return this.recoverPasswordUseCase;
    }

    getRefreshTokenUseCase(): RefreshTokenUseCase {
        return this.refreshTokenUseCase;
    }

    getRegisterUseCase(): RegisterUseCase {
        return this.registerUseCase;
    }
    getAuthUseCase(): Promise<boolean> {
        return this.authRepository.isAuthenticated?.() ?? false;
    }
    getCurrentUserUseCase(): Promise<User | null> {
        return this.authRepository.getCurrentUser?.() ?? null;
    }
}

// Singleton para evitar múltiples instancias
const authContainer = new AuthContainer();

export default authContainer;
