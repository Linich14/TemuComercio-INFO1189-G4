namespace Domain.Entities
{
    /// <summary>
    /// Entidad de dominio que representa una sesión de usuario activa.
    /// Contiene la lógica de negocio relacionada con sesiones.
    /// </summary>
    public class UserSession
    {
        public string SessionId { get; private set; } = null!;
        public int UserId { get; private set; }
        public string UserRut { get; private set; } = null!;
        public string UserEmail { get; private set; } = null!;
        public DateTime CreatedAt { get; private set; }
        public DateTime ExpiresAt { get; private set; }
        public bool IsActive { get; private set; }

        // Constructor privado para control de creación
        private UserSession() { }

        private UserSession(string sessionId, int userId, string userRut, string userEmail, 
                           DateTime expiresAt)
        {
            SessionId = sessionId;
            UserId = userId;
            UserRut = userRut;
            UserEmail = userEmail;
            CreatedAt = DateTime.UtcNow;
            ExpiresAt = expiresAt;
            IsActive = true;
        }

        /// <summary>
        /// Factory method para crear una nueva sesión.
        /// </summary>
        public static UserSession Create(User user, bool rememberMe = false)
        {
            var sessionId = Guid.NewGuid().ToString();
            var expirationHours = rememberMe ? 24 * 30 : 24; // 30 días o 1 día
            var expiresAt = DateTime.UtcNow.AddHours(expirationHours);

            return new UserSession(
                sessionId, 
                user.Id, 
                user.Rut.Value, 
                user.Email.Value,
                expiresAt
            );
        }

        /// <summary>
        /// Verifica si la sesión está válida (activa y no expirada).
        /// </summary>
        public bool IsValid()
        {
            return IsActive && DateTime.UtcNow < ExpiresAt;
        }

        /// <summary>
        /// Extiende la duración de la sesión.
        /// </summary>
        public void ExtendSession(int additionalHours = 24)
        {
            if (!IsValid())
                throw new InvalidOperationException("No se puede extender una sesión inválida");

            ExpiresAt = DateTime.UtcNow.AddHours(additionalHours);
        }

        /// <summary>
        /// Marca la sesión como inactiva (logout).
        /// </summary>
        public void Deactivate()
        {
            IsActive = false;
        }

        /// <summary>
        /// Calcula los minutos restantes hasta la expiración.
        /// </summary>
        public int GetRemainingMinutes()
        {
            if (!IsValid()) return 0;
            
            var remaining = ExpiresAt - DateTime.UtcNow;
            return (int)remaining.TotalMinutes;
        }
    }
}