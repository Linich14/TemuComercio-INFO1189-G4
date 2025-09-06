using Application.DTOs;

namespace Application.Interfaces
{
    /// <summary>
    /// Puerto (interface) para servicios de autenticación del frontend.
    /// Define el contrato que debe cumplir cualquier implementación de autenticación.
    /// Cumple con DIP: la UI no depende de implementaciones concretas.
    /// Cumple con ISP: interface específica para autenticación.
    /// </summary>
    public interface IAuthenticationService
    {
        /// <summary>
        /// Autentica un usuario con email y contraseña.
        /// </summary>
        Task<LoginResponseDto> LoginAsync(LoginRequestDto request);

        /// <summary>
        /// Cierra la sesión de un usuario.
        /// </summary>
        Task<bool> LogoutAsync(string sessionId);

        /// <summary>
        /// Valida si una sesión está activa.
        /// </summary>
        Task<bool> IsSessionValidAsync(string sessionId);

        /// <summary>
        /// Obtiene los datos de la sesión actual.
        /// </summary>
        Task<UserSessionDto?> GetCurrentSessionAsync(string sessionId);

        /// <summary>
        /// Extiende la duración de una sesión.
        /// </summary>
        Task<bool> ExtendSessionAsync(string sessionId);
    }
}
