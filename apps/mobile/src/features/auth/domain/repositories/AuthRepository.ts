import type { User } from "../entities/User";
export interface AuthRepository {
  login(params: { email: string; password: string }): Promise<{ user: User }>;
}
