import { Email } from '../value-objects/Email';
import { Rut } from '../value-objects/Rut';

export type User = {
    id: string;
    name: string;
    lastName: string;
    phone?: number;
    email: Email;
    run?: string;
    rut: Rut;
};
