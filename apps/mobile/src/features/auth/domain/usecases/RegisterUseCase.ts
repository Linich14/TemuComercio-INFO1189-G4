import { AuthRepository } from '../repositories/AuthRepository';
import { User } from '../entities/User';
import { Email } from '../value-objects/Email';
import { Password } from '../value-objects/Password';

export class RegisterUseCase {
    constructor(private repo: AuthRepository) {}
    execute(input: {
        name: string;
        phone: number;
        token: string;
        email: Email;
        password: Password;
    }): Promise<User> {
        return this.repo.register(input).then((result) => result.user);
    }
}
