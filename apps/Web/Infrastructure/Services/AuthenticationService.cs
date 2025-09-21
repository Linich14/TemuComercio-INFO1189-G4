using Application.DTOs;
using Application.Interfaces;
using Domain.Entities;
using Domain.Services;
using Domain.ValueObjects;

namespace Infrastructure.Services
{
    /// <summary>
    /// Implementación del servicio de autenticación usando arquitectura limpia.
    /// Utiliza servicios de dominio y maneja la conversión entre entidades y DTOs.
    /// </summary>
    public class AuthenticationService : IAuthenticationService
    {
        private readonly IAuthenticationDomainService _domainService;
        private readonly Dictionary<string, UserSession> _activeSessions; // Simulación temporal

        public AuthenticationService(IAuthenticationDomainService domainService)
        {
            _domainService = domainService;
            _activeSessions = new Dictionary<string, UserSession>();
        }

        /// <summary>
        /// Realiza el proceso de autenticación del usuario.
        /// </summary>
        public async Task<LoginResponseDto> LoginAsync(LoginRequestDto request)
        {
            try
            {
                // Simulación de latencia de red
                await Task.Delay(1000);
                
                // Validación de entrada
                if (string.IsNullOrWhiteSpace(request.Email) || string.IsNullOrWhiteSpace(request.Password))
                {
                    return LoginResponseDto.Failure("Email y contraseña son requeridos");
                }

                // Buscar usuario simulado
                var user = GetSimulatedUser(request.Email);
                if (user == null)
                {
                    return LoginResponseDto.Failure("Correo o contraseña incorrectos");
                }

                // Validar credenciales usando servicio de dominio
                if (!_domainService.ValidateCredentials(user, request.Password))
                {
                    return LoginResponseDto.Failure("Correo o contraseña incorrectos");
                }

                // Crear sesión usando servicio de dominio
                var session = _domainService.CreateSession(user, request.RememberMe);
                _activeSessions[session.SessionId] = session;

                // Convertir a DTO
                var sessionDto = MapToDto(session);
                
                return LoginResponseDto.Success(session.SessionId, sessionDto);
            }
            catch (Exception ex)
            {
                return LoginResponseDto.Failure($"Error de conexión: {ex.Message}");
            }
        }

        /// <summary>
        /// Cierra la sesión del usuario.
        /// </summary>
        public async Task<bool> LogoutAsync(string sessionId)
        {
            try
            {
                await Task.Delay(500);
                
                if (_activeSessions.TryGetValue(sessionId, out var session))
                {
                    session.Deactivate();
                    _activeSessions.Remove(sessionId);
                    return true;
                }
                
                return false;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Valida si una sesión está activa.
        /// </summary>
        public async Task<bool> IsSessionValidAsync(string sessionId)
        {
            try
            {
                await Task.Delay(300);
                
                if (_activeSessions.TryGetValue(sessionId, out var session))
                {
                    return session.IsValid();
                }
                
                return false;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Obtiene los datos de la sesión actual.
        /// </summary>
        public async Task<UserSessionDto?> GetCurrentSessionAsync(string sessionId)
        {
            try
            {
                await Task.Delay(300);
                
                if (_activeSessions.TryGetValue(sessionId, out var session) && session.IsValid())
                {
                    return MapToDto(session);
                }
                
                return null;
            }
            catch
            {
                return null;
            }
        }

        /// <summary>
        /// Extiende la duración de una sesión.
        /// </summary>
        public async Task<bool> ExtendSessionAsync(string sessionId)
        {
            try
            {
                await Task.Delay(300);
                
                if (_activeSessions.TryGetValue(sessionId, out var session))
                {
                    session.ExtendSession();
                    return true;
                }
                
                return false;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Registra un nuevo usuario en el sistema.
        /// </summary>
        public async Task<bool> RegisterUserAsync(UserRegistrationDto request)
        {
            try
            {
                await Task.Delay(1500);
                
                // Validación usando servicio de dominio
                bool canRegister = _domainService.CanRegisterUser(request.Rut, request.Email);
                
                if (!canRegister)
                {
                    return false;
                }

                // Verificar que el usuario no exista (simulado)
                bool emailTaken = IsEmailTaken(request.Email);
                
                if (emailTaken)
                {
                    return false;
                }

                // En una implementación real, aquí se guardaría en la base de datos
                // var hashedPassword = _domainService.HashPassword(request.Password);
                // var user = User.Create(request.Rut, request.Email, hashedPassword, request.RoleId);
                // await _userRepository.AddAsync(user);
                
                return true;
            }
            catch
            {
                return false;
            }
        }

        #region Métodos Privados - Simulación Temporal

        /// <summary>
        /// Obtiene un usuario simulado para demo.
        /// En producción se consultaría la base de datos.
        /// </summary>
        private User? GetSimulatedUser(string email)
        {
            var simulatedUsers = new Dictionary<string, (string rut, string password, int roleId)>
            {
                { "admin@temucomercio.cl", ("12345678-9", "admin123", 1) },
                { "demo@temucomercio.cl", ("87654321-0", "demo123", 2) },
                { "test@temucomercio.cl", ("11111111-1", "test123", 2) }
            };

            if (simulatedUsers.TryGetValue(email.ToLowerInvariant(), out var userData))
            {
                var hashedPassword = _domainService.HashPassword(userData.password);
                return User.Create(userData.rut, email, hashedPassword, userData.roleId);
            }

            return null;
        }

        /// <summary>
        /// Verifica si un email ya está en uso (simulado).
        /// </summary>
        private bool IsEmailTaken(string email)
        {
            var takenEmails = new[]
            {
                "admin@temucomercio.cl",
                "demo@temucomercio.cl", 
                "test@temucomercio.cl"
            };
            
            return takenEmails.Contains(email.ToLowerInvariant());
        }

        /// <summary>
        /// Convierte una entidad UserSession a DTO.
        /// </summary>
        private UserSessionDto MapToDto(UserSession session)
        {
            return new UserSessionDto
            {
                SessionId = session.SessionId,
                UserId = session.UserId,
                UserRut = session.UserRut,
                UserEmail = session.UserEmail,
                UserName = session.UserName,
                CreatedAt = session.CreatedAt,
                ExpiresAt = session.ExpiresAt
            };
        }

        /// <summary>
        /// Obtiene el nombre del rol según su ID.
        /// </summary>
        private string GetRoleName(int roleId)
        {
            return roleId switch
            {
                1 => "Administrador",
                2 => "Municipal",
                3 => "Fiscalizador",
                _ => "Desconocido"
            };
        }

        #endregion
    }
}