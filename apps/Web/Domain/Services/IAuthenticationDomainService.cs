using Domain.Entities;

namespace Domain.Services
{
    /// <summary>
    /// Interfaz para servicios de dominio relacionados con autenticación.
    /// Define las operaciones de dominio puras sin dependencias externas.
    /// </summary>
    public interface IAuthenticationDomainService
    {
        /// <summary>
        /// Verifica si las credenciales son válidas para un usuario.
        /// </summary>
        bool ValidateCredentials(User user, string password);

        /// <summary>
        /// Genera un hash seguro para una contraseña.
        /// </summary>
        string HashPassword(string password);

        /// <summary>
        /// Crea una nueva sesión de usuario.
        /// </summary>
        UserSession CreateSession(User user, bool rememberMe = false);

        /// <summary>
        /// Valida si un usuario puede registrarse (reglas de negocio).
        /// </summary>
        bool CanRegisterUser(string rut, string email);
    }
}