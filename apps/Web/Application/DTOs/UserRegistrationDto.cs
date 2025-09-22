using System.ComponentModel.DataAnnotations;

namespace Application.DTOs
{
    /// <summary>
    /// DTO (Data Transfer Object) para el registro de usuarios por parte del administrador.
    /// Contiene los datos necesarios para crear un nuevo usuario en el sistema.
    /// Este es un componente temporal para que los administradores puedan agregar usuarios de muestra.
    /// Los campos usua_creado, usua_actualizado, usua_estado y rous_id se manejan en el backend.
    /// </summary>
    public class UserRegistrationDto
    {
        /// <summary>
        /// RUT del usuario (usua_rut en BD)
        /// Campo obligatorio con validación de formato chileno
        /// </summary>
        [Required(ErrorMessage = "El RUT es obligatorio")]
        [StringLength(25, ErrorMessage = "El RUT no puede exceder 25 caracteres")]
        [RegularExpression(@"^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$|^\d{1,4}\.\d{3}-[\dkK]$|^\d{1,4}-[\dkK]$", ErrorMessage = "Formato de RUT inválido (ej: 12.345.678-9)")]
        public string Rut { get; set; } = string.Empty;

        /// <summary>
        /// Correo electrónico del usuario (usua_email en BD)
        /// Campo obligatorio con validación de formato
        /// Debe ser único en el sistema
        /// </summary>
        [Required(ErrorMessage = "El correo es obligatorio")]
        [EmailAddress(ErrorMessage = "Formato de correo inválido (ej: usuario@dominio.com)")]
        [StringLength(200, ErrorMessage = "El correo no puede exceder 200 caracteres")]
        public string Email { get; set; } = string.Empty;

        /// <summary>
        /// Contraseña del usuario (usua_pass en BD)
        /// Debe cumplir requisitos de seguridad: mínimo 8 caracteres, mayúscula, minúscula, número y símbolo
        /// Se encriptará en el backend antes de almacenar
        /// </summary>
        [Required(ErrorMessage = "La contraseña es obligatoria")]
        [MinLength(8, ErrorMessage = "La contraseña debe tener al menos 8 caracteres")]
        [StringLength(128, ErrorMessage = "La contraseña no puede exceder 128 caracteres")]
        [RegularExpression(@"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", 
            ErrorMessage = "La contraseña debe contener al menos: 8 caracteres, 1 mayúscula, 1 minúscula, 1 número y 1 símbolo (@$!%*?&)")]
        public string Password { get; set; } = string.Empty;

        /// <summary>
        /// Confirmación de contraseña
        /// Debe coincidir con la contraseña ingresada
        /// Este campo no se envía al backend, solo para validación en frontend
        /// </summary>
        [Required(ErrorMessage = "La confirmación de contraseña es obligatoria")]
        [Compare("Password", ErrorMessage = "Las contraseñas no coinciden")]
        public string ConfirmPassword { get; set; } = string.Empty;

        /// <summary>
        /// ID del rol del usuario (rous_id en BD)
        /// 1 = Administrador, 2 = Municipal, 3 = Fiscalizador
        /// </summary>
        [Required(ErrorMessage = "El rol es obligatorio")]
        [Range(1, 3, ErrorMessage = "Debe seleccionar un rol válido")]
        public int RoleId { get; set; } = 2; // Por defecto Municipal
    }
}