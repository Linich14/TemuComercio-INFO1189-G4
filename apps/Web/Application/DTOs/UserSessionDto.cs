namespace Application.DTOs
{
    /// <summary>
    /// DTO (Data Transfer Object) que representa los datos de sesión de un usuario autenticado.
    /// Contiene toda la información necesaria para mantener el estado de la sesión en el frontend.
    /// Se utiliza para transferir datos de sesión entre frontend y backend.
    /// </summary>
    public class UserSessionDto
    {
        /// <summary>
        /// Identificador único de la sesión
        /// Se genera cuando el usuario inicia sesión y se usa para validar todas las operaciones
        /// </summary>
        public string SessionId { get; set; } = string.Empty;
        
        /// <summary>
        /// ID único del usuario en la base de datos
        /// Referencia al registro del usuario en el sistema
        /// </summary>
        public int UserId { get; set; }
        
        /// <summary>
        /// RUT del usuario en formato chileno (ej: 12345678-9)
        /// Identificador único del usuario en el contexto chileno
        /// </summary>
        public string UserRut { get; set; } = string.Empty;
        
        /// <summary>
        /// Nombre completo del usuario (nombre + apellido)
        /// Se muestra en la interfaz para personalizar la experiencia
        /// </summary>
        public string UserName { get; set; } = string.Empty;
        
        /// <summary>
        /// Dirección de correo electrónico del usuario
        /// Puede utilizarse para notificaciones o recuperación de cuenta
        /// </summary>
        public string UserEmail { get; set; } = string.Empty;
        
        /// <summary>
        /// Fecha y hora cuando se creó la sesión
        /// Útil para auditoría y control de sesiones
        /// </summary>
        public DateTime CreatedAt { get; set; }
        
        /// <summary>
        /// Fecha y hora cuando expira la sesión
        /// Determina hasta cuándo es válida la sesión sin reautenticación
        /// </summary>
        public DateTime ExpiresAt { get; set; }
        
        /// <summary>
        /// Indica si la sesión está activa
        /// false = sesión cerrada o invalidada, true = sesión válida
        /// </summary>
        public bool IsActive { get; set; }
    }
}
