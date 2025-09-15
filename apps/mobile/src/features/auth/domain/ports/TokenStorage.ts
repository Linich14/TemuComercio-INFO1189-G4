export interface TokenStorage {
    saveToken(token: string): Promise<void>;
    getToken(): Promise<string | null>;
    deleteToken(): Promise<void>;
}
