using Application.DTOs;
using Domain.ValueObjects;

namespace Application.Validators
{
    /// <summary>
    /// Validador para solicitudes de login.
    /// Centraliza la validación de reglas de negocio y formato.
    /// </summary>
    public class LoginRequestValidator
    {
        /// <summary>
        /// Valida una solicitud de login completa.
        /// </summary>
        public ValidationResult Validate(LoginRequestDto request)
        {
            var result = new ValidationResult();

            if (request == null)
            {
                result.AddError("La solicitud no puede ser nula");
                return result;
            }

            // Validar email
            ValidateEmail(request.Email, result);

            // Validar contraseña
            ValidatePassword(request.Password, result);

            return result;
        }

        /// <summary>
        /// Valida el formato y reglas del email.
        /// </summary>
        private void ValidateEmail(string email, ValidationResult result)
        {
            if (string.IsNullOrWhiteSpace(email))
            {
                result.AddError("El email es obligatorio");
                return;
            }

            if (!Email.TryCreate(email, out _))
            {
                result.AddError("El formato del email es inválido");
            }
        }

        /// <summary>
        /// Valida la contraseña según reglas de negocio.
        /// </summary>
        private void ValidatePassword(string password, ValidationResult result)
        {
            if (string.IsNullOrWhiteSpace(password))
            {
                result.AddError("La contraseña es obligatoria");
                return;
            }

            if (password.Length < 6)
            {
                result.AddError("La contraseña debe tener al menos 6 caracteres");
            }

            if (password.Length > 128)
            {
                result.AddError("La contraseña no puede exceder 128 caracteres");
            }
        }
    }
}