import { AuthRepository } from '../repositories/AuthRepository';
import { User } from '../entities/User';

export class RegisterUseCase {
    constructor(private repo: AuthRepository) {}
    execute(input: { token: string }): Promise<User> {
        return this.repo
            .refreshToken(input.token)
            .then((result) => result.user);
    }
}
