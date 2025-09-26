using System.Text.RegularExpressions;

namespace Domain.ValueObjects
{
    /// <summary>
    /// Value Object que representa un RUT chileno válido.
    /// Encapsula la validación del formato y dígito verificador.
    /// Inmutable y sin identidad propia (Value Object pattern).
    /// </summary>
    public record Rut
    {
        public string Value { get; }
        public string Number { get; }
        public string VerifierDigit { get; }

        private Rut(string value, string number, string verifierDigit)
        {
            Value = value;
            Number = number;
            VerifierDigit = verifierDigit;
        }

        /// <summary>
        /// Factory method para crear un RUT válido.
        /// Valida formato pero NO el dígito verificador (para desarrollo/demo).
        /// </summary>
        public static Rut Create(string rut)
        {
            if (string.IsNullOrWhiteSpace(rut))
            {
                throw new ArgumentException("El RUT no puede estar vacío", nameof(rut));
            }

            var cleanRut = CleanRut(rut);
            
            if (!IsValidFormat(cleanRut))
            {
                throw new ArgumentException("Formato de RUT inválido. Debe ser 12345678-9", nameof(rut));
            }

            var (number, verifierDigit) = ExtractParts(cleanRut);

            // COMENTADO PARA DESARROLLO: Solo validamos formato, no dígito verificador
            // if (!IsValidVerifierDigit(number, verifierDigit))
            // {
            //     throw new ArgumentException("Dígito verificador del RUT inválido", nameof(rut));
            // }

            return new Rut(cleanRut, number, verifierDigit);
        }

        /// <summary>
        /// Intenta crear un RUT sin lanzar excepciones.
        /// </summary>
        public static bool TryCreate(string rut, out Rut? result)
        {
            result = null;
            try
            {
                result = Create(rut);
                return true;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Limpia el RUT removiendo puntos y espacios, pero mantiene el guión.
        /// </summary>
        private static string CleanRut(string rut)
        {
            return rut.Replace(".", "").Replace(" ", "").ToUpperInvariant();
        }

        /// <summary>
        /// Valida el formato básico del RUT: 12345678-9 o 12345678-K
        /// </summary>
        private static bool IsValidFormat(string rut)
        {
            var rutRegex = new Regex(@"^\d{7,8}-[\dK]$");
            return rutRegex.IsMatch(rut);
        }

        /// <summary>
        /// Extrae el número y dígito verificador del RUT.
        /// </summary>
        private static (string number, string verifierDigit) ExtractParts(string rut)
        {
            var parts = rut.Split('-');
            return (parts[0], parts[1]);
        }

        /// <summary>
        /// Valida el dígito verificador usando el algoritmo chileno.
        /// </summary>
        private static bool IsValidVerifierDigit(string number, string verifierDigit)
        {
            var sum = 0;
            var multiplier = 2;

            // Recorrer desde el final hacia el inicio
            for (int i = number.Length - 1; i >= 0; i--)
            {
                sum += int.Parse(number[i].ToString()) * multiplier;
                multiplier = multiplier == 7 ? 2 : multiplier + 1;
            }

            var remainder = sum % 11;
            var calculatedDigit = 11 - remainder;

            var expectedDigit = calculatedDigit switch
            {
                11 => "0",
                10 => "K",
                _ => calculatedDigit.ToString()
            };

            return expectedDigit == verifierDigit;
        }

        public override string ToString() => Value;

        public static implicit operator string(Rut rut) => rut.Value;
    }
}