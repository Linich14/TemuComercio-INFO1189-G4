export class Password {
    private constructor(private readonly value: string) {}
    static create(password: string): Password {
        if (!this.isValid(password)) throw new Error('Contraseña inválida');
        return new Password(password);
    }
    toString() {
        return this.value;
    }

    private static isValid(value: string): boolean {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    }
}
