using Application.DTOs;
using Domain.ValueObjects;

namespace Application.Validators
{
    /// <summary>
    /// Validador para solicitudes de registro de usuario.
    /// Centraliza la validación de reglas de negocio y formato.
    /// </summary>
    public class UserRegistrationValidator
    {
        /// <summary>
        /// Valida una solicitud de registro completa.
        /// </summary>
        public ValidationResult Validate(UserRegistrationDto request)
        {
            var result = new ValidationResult();

            if (request == null)
            {
                result.AddError("La solicitud no puede ser nula");
                return result;
            }

            // Validar RUT
            ValidateRut(request.Rut, result);

            // Validar email
            ValidateEmail(request.Email, result);

            // Validar contraseña
            ValidatePassword(request.Password, result);

            // Validar confirmación de contraseña
            ValidatePasswordConfirmation(request.Password, request.ConfirmPassword, result);

            // Validar rol
            ValidateRole(request.RoleId, result);

            return result;
        }

        /// <summary>
        /// Valida el formato y reglas del RUT.
        /// </summary>
        private void ValidateRut(string rut, ValidationResult result)
        {
            if (string.IsNullOrWhiteSpace(rut))
            {
                result.AddError("El RUT es obligatorio");
                return;
            }

            if (!Rut.TryCreate(rut, out _))
            {
                result.AddError("El formato del RUT es inválido o el dígito verificador no coincide");
            }
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

            if (email.Length > 200)
            {
                result.AddError("El email no puede exceder 200 caracteres");
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

            // Reglas adicionales de seguridad
            if (!HasValidPasswordComplexity(password))
            {
                result.AddError("La contraseña debe contener al menos una letra y un número");
            }
        }

        /// <summary>
        /// Valida que la confirmación de contraseña coincida.
        /// </summary>
        private void ValidatePasswordConfirmation(string password, string confirmPassword, ValidationResult result)
        {
            if (string.IsNullOrWhiteSpace(confirmPassword))
            {
                result.AddError("La confirmación de contraseña es obligatoria");
                return;
            }

            if (password != confirmPassword)
            {
                result.AddError("Las contraseñas no coinciden");
            }
        }

        /// <summary>
        /// Verifica que la contraseña tenga complejidad mínima.
        /// </summary>
        private bool HasValidPasswordComplexity(string password)
        {
            var hasLetter = password.Any(char.IsLetter);
            var hasDigit = password.Any(char.IsDigit);

            return hasLetter && hasDigit;
        }

        /// <summary>
        /// Valida que el rol seleccionado sea válido.
        /// </summary>
        private void ValidateRole(int roleId, ValidationResult result)
        {
            if (roleId < 1 || roleId > 3)
            {
                result.AddError("Debe seleccionar un rol válido (Administrador, Municipal o Fiscalizador)");
            }
        }
    }
}