using Domain.ValueObjects;

namespace Domain.Entities
{
    /// <summary>
    /// Entidad de dominio que representa un usuario en el sistema.
    /// Contiene la lógica de negocio relacionada con usuarios.
    /// </summary>
    public class User
    {
        public int Id { get; private set; }
        public Rut Rut { get; private set; } = null!;
        public Email Email { get; private set; } = null!;
        public string PasswordHash { get; private set; } = null!;
        public DateTime CreatedAt { get; private set; }
        public DateTime? UpdatedAt { get; private set; }
        public bool IsActive { get; private set; }
        public int RoleId { get; private set; }

        // Constructor privado para EF Core y factory methods
        private User() { }

        private User(Rut rut, Email email, string passwordHash, int roleId)
        {
            Rut = rut;
            Email = email;
            PasswordHash = passwordHash;
            RoleId = roleId;
            CreatedAt = DateTime.UtcNow;
            IsActive = true;
        }

        /// <summary>
        /// Factory method para crear un nuevo usuario.
        /// </summary>
        public static User Create(string rut, string email, string passwordHash, int roleId = 1)
        {
            var rutValue = Rut.Create(rut);
            var emailValue = Email.Create(email);

            if (string.IsNullOrWhiteSpace(passwordHash))
                throw new ArgumentException("El hash de contraseña no puede estar vacío", nameof(passwordHash));

            return new User(rutValue, emailValue, passwordHash, roleId);
        }

        /// <summary>
        /// Actualiza el email del usuario.
        /// </summary>
        public void UpdateEmail(string newEmail)
        {
            Email = Email.Create(newEmail);
            UpdatedAt = DateTime.UtcNow;
        }

        /// <summary>
        /// Actualiza la contraseña del usuario.
        /// </summary>
        public void UpdatePassword(string newPasswordHash)
        {
            if (string.IsNullOrWhiteSpace(newPasswordHash))
                throw new ArgumentException("El hash de contraseña no puede estar vacío", nameof(newPasswordHash));

            PasswordHash = newPasswordHash;
            UpdatedAt = DateTime.UtcNow;
        }

        /// <summary>
        /// Activa o desactiva el usuario.
        /// </summary>
        public void SetActiveStatus(bool isActive)
        {
            IsActive = isActive;
            UpdatedAt = DateTime.UtcNow;
        }

        /// <summary>
        /// Verifica si el usuario puede iniciar sesión.
        /// </summary>
        public bool CanLogin()
        {
            return IsActive;
        }
    }
}