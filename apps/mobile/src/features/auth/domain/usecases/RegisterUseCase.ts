import { AuthRepository } from '../repositories/AuthRepository';
import { Rut } from '../value-objects/Rut';
import { Email } from '../value-objects/Email';
import { Password } from '../value-objects/Password';
import { User } from '../entities/User';

export class RegisterUseCase {
    constructor(private repo: AuthRepository) {}
    execute(input: {
        name: string;
        lastName: string;
        phone?: number;
        email: Email;
        run?: string;
        rut: Rut;
        password: Password;
    }): Promise<User> {
        return this.repo.register(input).then((result) => result);
    }
}
