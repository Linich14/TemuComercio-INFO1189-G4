using System.Text.RegularExpressions;

namespace Domain.ValueObjects
{
    /// <summary>
    /// Value Object que representa un email válido.
    /// Encapsula la validación y garantiza que siempre contiene un email válido.
    /// Inmutable y sin identidad propia (Value Object pattern).
    /// </summary>
    public record Email
    {
        public string Value { get; }

        private Email(string value)
        {
            Value = value;
        }

        /// <summary>
        /// Factory method para crear un Email válido.
        /// Lanza excepción si el formato no es válido.
        /// </summary>
        public static Email Create(string email)
        {
            if (string.IsNullOrWhiteSpace(email))
                throw new ArgumentException("El email no puede estar vacío", nameof(email));

            if (!IsValidFormat(email))
                throw new ArgumentException("Formato de email inválido", nameof(email));

            return new Email(email.ToLowerInvariant().Trim());
        }

        /// <summary>
        /// Intenta crear un Email sin lanzar excepciones.
        /// </summary>
        public static bool TryCreate(string email, out Email? result)
        {
            result = null;
            try
            {
                result = Create(email);
                return true;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Valida el formato del email usando regex.
        /// </summary>
        private static bool IsValidFormat(string email)
        {
            var emailRegex = new Regex(@"^[^@\s]+@[^@\s]+\.[^@\s]+$", RegexOptions.IgnoreCase);
            return emailRegex.IsMatch(email);
        }

        public override string ToString() => Value;

        public static implicit operator string(Email email) => email.Value;
    }
}