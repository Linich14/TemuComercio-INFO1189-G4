import type { AuthRepository } from "../repositories/AuthRepository";
import type { User } from "../entities/User";

export class LoginUseCase {
  constructor(private repo: AuthRepository) {}
  execute(input: { email: string; password: string }): Promise<User> {
    return this.repo.login(input).then(r => r.user);
  }
}
