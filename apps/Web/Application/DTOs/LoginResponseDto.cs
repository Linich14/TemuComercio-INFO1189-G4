namespace Application.DTOs
{
    /// <summary>
    /// DTO (Data Transfer Object) para la respuesta del proceso de inicio de sesión.
    /// Contiene el resultado de la autenticación y los datos de sesión si fue exitosa.
    /// Se utiliza para transferir datos desde el backend hacia el frontend.
    /// </summary>
    public class LoginResponseDto
    {
        /// <summary>
        /// Indica si el proceso de login fue exitoso
        /// true = login correcto, false = login fallido
        /// </summary>
        public bool IsSuccess { get; set; }
        
        /// <summary>
        /// Mensaje descriptivo del resultado del login
        /// Ej: "Inicio de sesión exitoso" o "RUT o contraseña incorrectos"
        /// </summary>
        public string Message { get; set; } = string.Empty;
        
        /// <summary>
        /// Token de sesión generado por el backend (solo si el login fue exitoso)
        /// Este token se almacena en la tabla Sesion_Token y debe enviarse en requests subsecuentes
        /// </summary>
        public string? Token { get; set; }
        
        /// <summary>
        /// Fecha de expiración del token en formato UTC (solo si el login fue exitoso)
        /// Permite al frontend saber cuándo renovar o solicitar nuevo login
        /// </summary>
        public DateTime? TokenExpiresAt { get; set; }
        
        /// <summary>
        /// ID único de la sesión generada (solo si el login fue exitoso)
        /// Se utiliza para mantener el estado de autenticación del usuario
        /// </summary>
        public string? SessionId { get; set; }
        
        /// <summary>
        /// Datos completos de la sesión del usuario (solo si el login fue exitoso)
        /// Incluye información del usuario y configuración de la sesión
        /// </summary>
        public UserSessionDto? UserSession { get; set; }
        
        /// <summary>
        /// Lista de errores específicos que ocurrieron durante el proceso
        /// Útil para mostrar múltiples mensajes de validación al usuario
        /// </summary>
        public List<string> Errors { get; set; } = new();
        
        #region Factory Methods
        
        /// <summary>
        /// Método factory para crear una respuesta de login exitoso
        /// Simplifica la creación de respuestas positivas con datos consistentes
        /// </summary>
        /// <param name="token">Token de sesión generado</param>
        /// <param name="tokenExpiresAt">Fecha de expiración del token</param>
        /// <param name="sessionId">ID de la sesión generada</param>
        /// <param name="userSession">Datos de la sesión del usuario</param>
        /// <returns>LoginResponseDto configurado para éxito</returns>
        public static LoginResponseDto Success(string token, DateTime tokenExpiresAt, string sessionId, UserSessionDto userSession)
        {
            return new LoginResponseDto
            {
                IsSuccess = true,
                Message = "Inicio de sesión exitoso",
                Token = token,
                TokenExpiresAt = tokenExpiresAt,
                SessionId = sessionId,
                UserSession = userSession
            };
        }
        
        /// <summary>
        /// Método factory para crear una respuesta de login fallido
        /// Simplifica la creación de respuestas de error con mensajes consistentes
        /// </summary>
        /// <param name="message">Mensaje de error principal</param>
        /// <param name="errors">Lista opcional de errores específicos</param>
        /// <returns>LoginResponseDto configurado para fallo</returns>
        public static LoginResponseDto Failure(string message, List<string>? errors = null)
        {
            return new LoginResponseDto
            {
                IsSuccess = false,
                Message = message,
                Errors = errors ?? new List<string>()
            };
        }
        
        #endregion
    }
}
