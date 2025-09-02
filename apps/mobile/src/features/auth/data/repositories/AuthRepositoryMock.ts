import type { AuthRepository } from "../../domain/repositories/AuthRepository";
import type { User } from "../../domain/entities/User";

export class AuthRepositoryMock implements AuthRepository {
  async login({ email, password }: { email: string; password: string }): Promise<{ user: User }> {
    await new Promise(r => setTimeout(r, 600));
    if (password !== "123456") throw new Error("Credenciales inválidas");
    return { user: { id: "1", name: "Demo", email, token: "fake" } };
  }
}
