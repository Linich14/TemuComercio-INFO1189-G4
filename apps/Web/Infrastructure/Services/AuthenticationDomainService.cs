using Domain.Entities;
using Domain.Services;
using Domain.ValueObjects;

namespace Infrastructure.Services
{
    /// <summary>
    /// Implementación de servicios de dominio para autenticación.
    /// Contiene la lógica de negocio pura sin dependencias externas.
    /// </summary>
    public class AuthenticationDomainService : IAuthenticationDomainService
    {
        /// <summary>
        /// Verifica si las credenciales son válidas para un usuario.
        /// </summary>
        public bool ValidateCredentials(User user, string password)
        {
            if (user == null || !user.CanLogin())
                return false;

            // En un escenario real, aquí se verificaría el hash de la contraseña
            // Por ahora usamos validación simple para demo
            return VerifyPassword(password, user.PasswordHash);
        }

        /// <summary>
        /// Genera un hash seguro para una contraseña.
        /// En producción se usaría BCrypt o similar.
        /// </summary>
        public string HashPassword(string password)
        {
            if (string.IsNullOrWhiteSpace(password))
                throw new ArgumentException("La contraseña no puede estar vacía", nameof(password));

            // TEMPORAL: Hash simple para demo
            // En producción usar: BCrypt.Net.BCrypt.HashPassword(password)
            return Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(password + "_hashed"));
        }

        /// <summary>
        /// Crea una nueva sesión de usuario.
        /// </summary>
        public UserSession CreateSession(User user, bool rememberMe = false)
        {
            if (user == null)
                throw new ArgumentNullException(nameof(user));

            if (!user.CanLogin())
                throw new InvalidOperationException("El usuario no puede iniciar sesión");

            return UserSession.Create(user, rememberMe);
        }

        /// <summary>
        /// Valida si un usuario puede registrarse según reglas de negocio.
        /// </summary>
        public bool CanRegisterUser(string rut, string email)
        {
            // Validar que el RUT y email tengan formato válido
            if (!Rut.TryCreate(rut, out _))
                return false;

            if (!Email.TryCreate(email, out _))
                return false;

            // Reglas de negocio adicionales
            // Por ejemplo: verificar que no sea un email temporal, etc.
            return true;
        }

        /// <summary>
        /// Verifica si una contraseña coincide con su hash.
        /// </summary>
        private bool VerifyPassword(string password, string hash)
        {
            if (string.IsNullOrWhiteSpace(password) || string.IsNullOrWhiteSpace(hash))
                return false;

            // TEMPORAL: Verificación simple para demo
            // En producción usar: BCrypt.Net.BCrypt.Verify(password, hash)
            var expectedHash = Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(password + "_hashed"));
            return hash == expectedHash;
        }
    }
}