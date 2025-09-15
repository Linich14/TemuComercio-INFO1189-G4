import * as SecureStore from 'expo-secure-store';
import { UserStorage } from '../../domain/ports/UserStorage';
import { User } from '../../domain/entities/User';

const USER_KEY = 'userData';

export class SecureUserStorage implements UserStorage {
    async saveUser(user: User): Promise<void> {
        await SecureStore.setItemAsync(USER_KEY, JSON.stringify(user));
    }

    async getUser(): Promise<User | null> {
        const userData = await SecureStore.getItemAsync(USER_KEY);
        return userData ? (JSON.parse(userData) as User) : null;
    }

    async deleteUser(): Promise<void> {
        await SecureStore.deleteItemAsync(USER_KEY);
    }
}
