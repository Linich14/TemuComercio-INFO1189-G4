import { Session } from '../../domain/entities/Session';
import { SessionDTO } from '../models/SessionDTO';
import { toDomainUser, toUserDTO } from './UserMapper';

export class SessionMapper {
    toDomain(dto: SessionDTO): Session {
        return {
            user: toDomainUser(dto.user),
            accessToken: dto.accessToken,
            refreshToken: dto.refreshToken,
            expiresAt: dto.expiresAt ? new Date(dto.expiresAt) : undefined,
        };
    }

    toDTO(domain: Session): SessionDTO {
        return {
            user: toUserDTO(domain.user),
            accessToken: domain.accessToken,
            refreshToken: domain.refreshToken,
            expiresAt: domain.expiresAt?.toISOString(),
        };
    }
}
