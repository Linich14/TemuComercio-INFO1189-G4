import type { AuthRepository } from '../repositories/AuthRepository';
import type { User } from '../entities/User';
import { Email } from '../value-objects/Email';
import { Password } from '../value-objects/Password';

export class LoginUseCase {
    constructor(private repo: AuthRepository) {}
    execute(input: { email: Email; password: Password }): Promise<User> {
        return this.repo.login(input).then((result) => result.user);
    }
}
