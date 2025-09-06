using Application.DTOs;
using Application.Interfaces;

namespace Application.Services
{
    /// <summary>
    /// Servicio de autenticación simplificado para frontend.
    /// Incluye simulación temporal para demo del login.
    /// Cumple con SRP: solo se encarga de autenticación.
    /// Cumple con DIP: implementa la interfaz IAuthenticationService.
    /// </summary>
    public class AuthenticationService : IAuthenticationService
    {
        /// <summary>
        /// Realiza el proceso de autenticación del usuario.
        /// TEMPORAL: Simula respuesta hasta que el backend esté listo.
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

                // Validar credenciales usando datos simulados
                if (IsValidLogin(request.Email, request.Password))
                {
                    var sessionId = Guid.NewGuid().ToString();
                    var userSession = CreateUserSession(sessionId, request);
                    
                    return LoginResponseDto.Success(sessionId, userSession);
                }
                else
                {
                    return LoginResponseDto.Failure("Correo o contraseña incorrectos");
                }
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
                return !string.IsNullOrEmpty(sessionId);
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
                return !string.IsNullOrEmpty(sessionId);
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
                
                if (string.IsNullOrEmpty(sessionId))
                    return null;

                return CreateDemoSession(sessionId);
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
                await Task.Delay(500);
                return !string.IsNullOrEmpty(sessionId);
            }
            catch
            {
                return false;
            }
        }

        #region Métodos de Simulación para Demo (Frontend Only), Ningun dato de aca sera usado en el backend y sera eliminado luego

        /// <summary>
        /// MÉTODO TEMPORAL: Valida credenciales usando datos hardcodeados para demo.
        /// </summary>
        private bool IsValidLogin(string email, string password)
        {
            var validUsers = new Dictionary<string, string>
            {
                { "admin@temucomercio.cl", "123456" },
                { "demo@temucomercio.cl", "password" },
                { "test@temucomercio.cl", "test123" }
            };

            return validUsers.ContainsKey(email.ToLowerInvariant()) && 
                   validUsers[email.ToLowerInvariant()] == password;
        }

        /// <summary>
        /// Crea un objeto de sesión de usuario para respuesta exitosa.
        /// </summary>
        private UserSessionDto CreateUserSession(string sessionId, LoginRequestDto request)
        {
            return new UserSessionDto
            {
                SessionId = sessionId,
                UserId = GetUserId(request.Email),
                UserEmail = request.Email,
                UserName = GetUserName(request.Email),
                CreatedAt = DateTime.UtcNow,
                ExpiresAt = DateTime.UtcNow.AddHours(request.RememberMe ? 720 : 24),
                IsActive = true
            };
        }

        /// <summary>
        /// Crea una sesión demo para validación.
        /// </summary>
        private UserSessionDto CreateDemoSession(string sessionId)
        {
            return new UserSessionDto
            {
                SessionId = sessionId,
                UserId = 1,
                UserEmail = "demo@temucomercio.cl",
                UserName = "Usuario Demo",
                CreatedAt = DateTime.UtcNow.AddHours(-2),
                ExpiresAt = DateTime.UtcNow.AddHours(22),
                IsActive = true
            };
        }

        /// <summary>
        /// Obtiene ID de usuario simulado.
        /// </summary>
        private int GetUserId(string email)
        {
            return email.ToLowerInvariant() switch
            {
                "admin@temucomercio.cl" => 1,
                "demo@temucomercio.cl" => 2,
                "test@temucomercio.cl" => 3,
                _ => 999
            };
        }

        /// <summary>
        /// Obtiene nombre de usuario simulado.
        /// </summary>
        private string GetUserName(string email)
        {
            return email.ToLowerInvariant() switch
            {
                "admin@temucomercio.cl" => "Admin Sistema",
                "demo@temucomercio.cl" => "Usuario Demo",
                "test@temucomercio.cl" => "Test User",
                _ => "Usuario"
            };
        }

        #endregion
    }
}
