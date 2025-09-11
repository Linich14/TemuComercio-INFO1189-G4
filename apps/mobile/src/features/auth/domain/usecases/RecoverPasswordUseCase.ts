import { AuthRepository } from '../repositories/AuthRepository';
import { Email } from '../value-objects/Email';

export class RecoverPasswordUseCase {
    constructor(private repo: AuthRepository) {}

    execute(input: { email: Email }): Promise<void> {
        return this.repo.recoverPassword(input.email);
    }
}
