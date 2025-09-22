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
        /// Valida si un token de sesión está activo y no ha expirado.
        /// Consulta al backend para verificar estado del token en tabla Sesion_Token.
        /// </summary>
        Task<bool> IsTokenValidAsync(string token);

        /// <summary>
        /// Cierra la sesión de un usuario usando su token.
        /// Invalida el token en el backend y limpia la sesión local.
        /// </summary>
        Task<bool> LogoutByTokenAsync(string token);

        /// <summary>
        /// Obtiene los datos de la sesión actual usando el token.
        /// Retorna información del usuario si el token es válido.
        /// </summary>
        Task<UserSessionDto?> GetSessionByTokenAsync(string token);

        /// <summary>
        /// Cierra la sesión de un usuario (método legacy con sessionId).
        /// </summary>
        Task<bool> LogoutAsync(string sessionId);

        /// <summary>
        /// Valida si una sesión está activa (método legacy con sessionId).
        /// </summary>
        Task<bool> IsSessionValidAsync(string sessionId);

        /// <summary>
        /// Obtiene los datos de la sesión actual (método legacy con sessionId).
        /// </summary>
        Task<UserSessionDto?> GetCurrentSessionAsync(string sessionId);

        /// <summary>
        /// Extiende la duración de una sesión.
        /// </summary>
        Task<bool> ExtendSessionAsync(string sessionId);

        /// <summary>
        /// Registra un nuevo usuario en el sistema (solo para administradores).
        /// Este es un método temporal para permitir el ingreso de usuarios de muestra.
        /// </summary>
        Task<bool> RegisterUserAsync(UserRegistrationDto request);
    }
}
