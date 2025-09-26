import { UserDTO } from './UserDTO';

export interface SessionDTO {
    user: UserDTO;
    access_token: string;
    refresh_token?: string;
    expires_at?: string;
    type?: string;
}
