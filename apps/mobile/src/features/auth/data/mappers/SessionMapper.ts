import { Session } from '../../domain/entities/Session';
import { SessionDTO } from '../models/SessionDTO';
import { toDomainUser, toUserDTO } from './UserMapper';

export class SessionMapper {
    static toDomain(dto: SessionDTO): Session {
        return {
            user: toDomainUser(dto.user),
            accessToken: dto.access_token,
            refreshToken: dto.refresh_token,
            expiresAt: dto.expires_at ? new Date(dto.expires_at) : undefined,
        };
    }

    static toDTO(domain: Session): SessionDTO {
        return {
            user: toUserDTO(domain.user),
            access_token: domain.accessToken,
            refresh_token: domain.refreshToken,
            expires_at: domain.expiresAt?.toISOString(),
        };
    }
}
