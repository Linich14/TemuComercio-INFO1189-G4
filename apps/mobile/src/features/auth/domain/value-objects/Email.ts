export class Email {
    private constructor(private readonly value: string) {}
    static create(email: string): Email {
        if (!this.isValid(email)) throw new Error('Email inválido');
        return new Email(email.toLowerCase());
    }
    toString(): string {
        return this.value;
    }

    private static isValid(value: string): boolean {
        const trimmed = value.trim();
        // Expresión regular más estricta para validar emails comunes
        return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(trimmed);
    }
}
