export interface TokenStorage {
    saveToken(): Promise<string | null>;
    getToken(): Promise<string | null>;
    deleteToken(): Promise<void>;
}
