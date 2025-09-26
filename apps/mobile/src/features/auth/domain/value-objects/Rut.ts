export class Rut {
    private constructor(private readonly value: string) {}

    static create(rut: string): Rut {
        const cleanRut = rut.replace(/\D/g, ''); // Solo números
        if (!this.isValid(cleanRut)) throw new Error('RUT inválido');
        return new Rut(cleanRut);
    }

    toString(): string {
        const rut = this.value;
        const cuerpo = rut.slice(0, -1);
        const dv = rut.slice(-1);
        return `${cuerpo}-${dv}`;
    }

    static isValid(value: string): boolean {
        // Debe tener 9 dígitos
        return /^\d{9}$/.test(value);
    }

    get length(): number {
        return this.value.length;
    }

    toJSON() {
        return this.value;
    }
}
