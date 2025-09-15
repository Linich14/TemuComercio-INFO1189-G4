import type { AuthRepository } from '../repositories/AuthRepository';
import { Email } from '../value-objects/Email';
import { Password } from '../value-objects/Password';
import { User } from '../entities/User';

export class LoginUseCase {
    constructor(private repo: AuthRepository) {}
    execute(input: { email: Email; password: Password }): Promise<User> {
        return this.repo.login(input);
    }
}
