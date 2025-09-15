import { User } from '../../domain/entities/User';
import { Email } from '../../domain/value-objects/Email';
import { Rut } from '../../domain/value-objects/Rut';
import { UserDTO } from '../models/UserDTO';

export function toUserDTO(user: User): UserDTO {
    return {
        id: user.id,
        name: user.name,
        lastName: user.lastName,
        phone: user.phone ?? null,
        email: user.email.toString(),
        run: user.run ?? null,
        rut: user.rut.getValue(),
    };
}

export function toDomainUser(dto: UserDTO): User {
    return {
        id: dto.id,
        name: dto.name,
        lastName: dto.lastName,
        phone: dto.phone ?? undefined,
        email: Email.create(dto.email),
        run: dto.run ?? undefined,
        rut: Rut.create(dto.rut),
    };
}
