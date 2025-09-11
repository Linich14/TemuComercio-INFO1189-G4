import * as SecureStore from 'expo-secure-store';
import { TokenStorage } from '../../domain/ports/TokenStorage';

const TOKEN_KEY = 'authToken';

export class SecureTokenStorage implements TokenStorage {
    async saveToken(token: string): Promise<void> {
        await SecureStore.setItemAsync(TOKEN_KEY, token);
    }

    async getToken(): Promise<string | null> {
        return await SecureStore.getItemAsync(TOKEN_KEY);
    }

    async deleteToken(): Promise<void> {
        await SecureStore.deleteItemAsync(TOKEN_KEY);
    }
}
