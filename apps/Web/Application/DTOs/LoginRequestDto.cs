using System.ComponentModel.DataAnnotations;

namespace Application.DTOs
{
    /// <summary>
    /// DTO (Data Transfer Object) para la solicitud de inicio de sesión.
    /// Contiene los datos necesarios que el usuario debe proporcionar para autenticarse.
    /// Se utiliza para transferir datos desde el frontend hacia el backend.
    /// </summary>
    public class LoginRequestDto
    {
    /// <summary>
    /// Correo electrónico del usuario
    /// Campo obligatorio con validación de formato
    /// </summary>
    [Required(ErrorMessage = "El correo es obligatorio")]
    [EmailAddress(ErrorMessage = "Formato de correo inválido (ej: usuario@dominio.com)")]
    public string Email { get; set; } = string.Empty;
        
        /// <summary>
        /// Contraseña del usuario
        /// Debe tener al menos 6 caracteres por seguridad mínima
        /// </summary>
        [Required(ErrorMessage = "La contraseña es obligatoria")]
        [MinLength(6, ErrorMessage = "La contraseña debe tener al menos 6 caracteres")]
        public string Password { get; set; } = string.Empty;
        
        /// <summary>
        /// Indica si el usuario desea mantener la sesión activa por más tiempo
        /// true = sesión extendida (30 días), false = sesión normal (1 día)
        /// </summary>
        public bool RememberMe { get; set; } = false;
    }
}
