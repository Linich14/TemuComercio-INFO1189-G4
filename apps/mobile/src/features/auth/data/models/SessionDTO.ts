import { UserDTO } from './UserDTO';

export interface SessionDTO {
    user: UserDTO;
    accessToken: string;
    refreshToken?: string;
    expiresAt?: string;
}
