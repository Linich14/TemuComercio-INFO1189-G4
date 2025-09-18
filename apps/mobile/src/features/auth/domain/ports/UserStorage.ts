import { User } from '../entities/User';

export interface UserStorage {
    saveUser(user: User): Promise<void>;
    getUser(): Promise<User | null>;
    deleteUser(): Promise<void>;
}
