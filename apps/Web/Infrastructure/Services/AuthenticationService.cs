using Application.DTOs;
using Application.Interfaces;
using Domain.Entities;
using Domain.Services;
using Domain.ValueObjects;
using System.Text;
using System.Text.Json;

namespace Infrastructure.Services
{
    /// <summary>
    /// Implementación del servicio de autenticación usando arquitectura limpia.
    /// Utiliza servicios de dominio y maneja la conversión entre entidades y DTOs.
    /// </summary>
    public class AuthenticationService : IAuthenticationService
    {
        private readonly IAuthenticationDomainService _domainService;
        private readonly HttpClient _httpClient;

        public AuthenticationService(IAuthenticationDomainService domainService, HttpClient httpClient)
        {
            _domainService = domainService;
            _httpClient = httpClient;
        }

        /// <summary>
        /// Realiza el proceso de autenticación del usuario conectándose al API Django.
        /// </summary>
        public async Task<LoginResponseDto> LoginAsync(LoginRequestDto request)
        {
            try
            {
                // Validación de entrada
                if (string.IsNullOrWhiteSpace(request.Email) || string.IsNullOrWhiteSpace(request.Password))
                {
                    return LoginResponseDto.Failure("Email y contraseña son requeridos");
                }

                // Preparar datos para envío al backend Django
                var loginData = new
                {
                    email = request.Email,
                    password = request.Password,
                    remember_me = request.RememberMe
                };

                // Serializar a JSON
                var jsonContent = JsonSerializer.Serialize(loginData);
                var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

                // Enviar solicitud POST al endpoint Django de login
                var response = await _httpClient.PostAsync("api/auth/login/", content);

                if (response.IsSuccessStatusCode)
                {
                    // 200 OK - Login exitoso, parsear respuesta
                    var responseContent = await response.Content.ReadAsStringAsync();
                    using var document = JsonDocument.Parse(responseContent);
                    var root = document.RootElement;
                    
                    // Verificar si tiene estructura con 'success' y 'data'
                    if (root.TryGetProperty("success", out var successElement) && 
                        IsSuccessValue(successElement) && 
                        root.TryGetProperty("data", out var dataElement))
                    {
                        // Estructura: { "success": true, "data": {...} }
                        return ParseLoginResponse(dataElement);
                    }
                    // Si no tiene 'success', pero sí tiene 'data', asumir éxito
                    else if (root.TryGetProperty("data", out var directDataElement))
                    {
                        // Estructura: { "data": {...} }
                        return ParseLoginResponse(directDataElement);
                    }
                    // Si la respuesta directamente tiene token y user
                    else if (root.TryGetProperty("token", out var _))
                    {
                        // Estructura directa: { "token": "...", "user": {...}, ... }
                        return ParseLoginResponse(root);
                    }
                    else
                    {
                        // Respuesta exitosa pero estructura desconocida
                        return LoginResponseDto.Failure("Estructura de respuesta no reconocida");
                    }
                }
                else if (response.StatusCode == System.Net.HttpStatusCode.Unauthorized)
                {
                    // 401 Unauthorized - Credenciales incorrectas
                    try
                    {
                        var errorContent = await response.Content.ReadAsStringAsync();
                        using var document = JsonDocument.Parse(errorContent);
                        var root = document.RootElement;
                        
                        if (root.TryGetProperty("message", out var messageElement))
                        {
                            var message = messageElement.GetString() ?? "Credenciales incorrectas";
                            return LoginResponseDto.Failure(message);
                        }
                    }
                    catch
                    {
                        // Si no se puede parsear la respuesta de error
                    }
                    
                    return LoginResponseDto.Failure("Correo o contraseña incorrectos");
                }
                else if (response.StatusCode == System.Net.HttpStatusCode.BadRequest)
                {
                    // 400 Bad Request - Datos inválidos
                    try
                    {
                        var errorContent = await response.Content.ReadAsStringAsync();
                        using var document = JsonDocument.Parse(errorContent);
                        var root = document.RootElement;
                        
                        var errors = new List<string>();
                        if (root.TryGetProperty("errors", out var errorsElement) && errorsElement.ValueKind == JsonValueKind.Array)
                        {
                            foreach (var error in errorsElement.EnumerateArray())
                            {
                                var errorText = error.GetString();
                                if (!string.IsNullOrEmpty(errorText))
                                    errors.Add(errorText);
                            }
                        }
                        
                        var message = root.TryGetProperty("message", out var messageElement) 
                            ? messageElement.GetString() ?? "Datos inválidos"
                            : "Datos inválidos";
                            
                        return LoginResponseDto.Failure(message, errors);
                    }
                    catch
                    {
                        return LoginResponseDto.Failure("Datos inválidos");
                    }
                }
                else
                {
                    // Otros códigos de error
                    return LoginResponseDto.Failure("Error en el servidor. Intente nuevamente.");
                }
            }
            catch (HttpRequestException)
            {
                return LoginResponseDto.Failure("Error de conexión con el servidor");
            }
            catch (JsonException)
            {
                return LoginResponseDto.Failure("Error al procesar la respuesta del servidor");
            }
            catch (Exception ex)
            {
                return LoginResponseDto.Failure($"Error inesperado: {ex.Message}");
            }
        }

        /// <summary>
        /// Cierra la sesión del usuario enviando el token al API Django.
        /// </summary>
        public async Task<bool> LogoutAsync(string token)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(token))
                    return false;

                // Configurar headers de autorización
                _httpClient.DefaultRequestHeaders.Authorization = 
                    new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

                // Llamar al endpoint de logout de Django
                var response = await _httpClient.PostAsync("api/auth/logout/", null);

                // Si el response es 200, el logout fue exitoso
                return response.IsSuccessStatusCode;
            }
            catch (HttpRequestException)
            {
                // Error de conexión, pero localmente podemos considerar logout exitoso
                return true;
            }
            catch (Exception)
            {
                // Cualquier otro error, consideramos logout fallido
                return false;
            }
        }

        /// <summary>
        /// Valida si un token está activo consultando al API Django.
        /// </summary>
        public async Task<bool> IsSessionValidAsync(string token)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(token))
                    return false;

                // Configurar headers de autorización
                _httpClient.DefaultRequestHeaders.Authorization = 
                    new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

                // Llamar al endpoint de verificación de Django
                var response = await _httpClient.GetAsync("api/auth/verify/");

                // Si el response es 200, el token es válido
                return response.IsSuccessStatusCode;
            }
            catch (HttpRequestException)
            {
                // Error de conexión, consideramos token inválido
                return false;
            }
            catch (Exception)
            {
                // Cualquier otro error, consideramos token inválido
                return false;
            }
        }

        /// <summary>
        /// Obtiene los datos de la sesión actual (método legacy con sessionId).
        /// </summary>
        public async Task<UserSessionDto?> GetCurrentSessionAsync(string sessionId)
        {
            try
            {
                await Task.Delay(300);
                // TODO: Implementar con API Django si es necesario
                return null;
            }
            catch
            {
                return null;
            }
        }

        /// <summary>
        /// Extiende la duración de una sesión (método legacy).
        /// </summary>
        public async Task<bool> ExtendSessionAsync(string sessionId)
        {
            try
            {
                await Task.Delay(300);
                // TODO: Implementar con API Django si es necesario
                return false;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Registra un nuevo usuario en el sistema conectándose al API Django.
        /// </summary>
        public async Task<bool> RegisterUserAsync(UserRegistrationDto request)
        {
            try
            {
                // Validación usando servicio de dominio local
                bool canRegister = _domainService.CanRegisterUser(request.Rut, request.Email);
                
                if (!canRegister)
                {
                    return false;
                }

                // Mapear a formato esperado por Django
                var djangoUser = new
                {
                    usua_rut = request.Rut,
                    usua_email = request.Email,
                    usua_pass = request.Password,
                    rous_id = request.RoleId
                };

                // Serializar a JSON
                var jsonContent = JsonSerializer.Serialize(djangoUser);
                var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

                // Enviar solicitud POST al endpoint Django
                var response = await _httpClient.PostAsync("api/usuarios/create/", content);

                // Verificar código de respuesta
                if (response.IsSuccessStatusCode)
                {
                    // 201 Created - Usuario registrado exitosamente
                    return true;
                }
                else if (response.StatusCode == System.Net.HttpStatusCode.BadRequest)
                {
                    // 400 Bad Request - RUT o email ya existe
                    var errorContent = await response.Content.ReadAsStringAsync();
                    // Log del error si es necesario para debugging
                    return false;
                }
                else
                {
                    // Otros códigos de error (422, 500, etc.)
                    return false;
                }
            }
            catch (HttpRequestException)
            {
                // Error de conexión con el API
                return false;
            }
            catch (JsonException)
            {
                // Error de serialización JSON
                return false;
            }
            catch
            {
                // Cualquier otro error
                return false;
            }
        }

        #region Métodos Utilitarios

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

        #region Métodos de Token Management

        /// <summary>
        /// Valida si un token de sesión está activo y no ha expirado.
        /// </summary>
        public async Task<bool> IsTokenValidAsync(string token)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(token))
                    return false;

                // Enviar solicitud GET al endpoint Django para validar token
                _httpClient.DefaultRequestHeaders.Authorization = 
                    new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

                var response = await _httpClient.GetAsync("api/auth/verify/");

                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Cierra la sesión de un usuario usando su token.
        /// </summary>
        public async Task<bool> LogoutByTokenAsync(string token)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(token))
                    return false;

                // Configurar header de autorización
                _httpClient.DefaultRequestHeaders.Authorization = 
                    new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

                // Enviar solicitud POST al endpoint Django para logout
                var response = await _httpClient.PostAsync("api/auth/logout/", null);

                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Obtiene los datos de la sesión actual usando el token.
        /// </summary>
        public async Task<UserSessionDto?> GetSessionByTokenAsync(string token)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(token))
                    return null;

                // Configurar header de autorización
                _httpClient.DefaultRequestHeaders.Authorization = 
                    new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

                // Enviar solicitud GET al endpoint Django para obtener datos de sesión
                var response = await _httpClient.GetAsync("api/auth/session/");

                if (response.IsSuccessStatusCode)
                {
                    var content = await response.Content.ReadAsStringAsync();
                    // TODO: Deserializar la respuesta JSON del backend Django
                    // Por ahora retornamos null hasta tener la estructura exacta
                    return null;
                }

                return null;
            }
            catch
            {
                return null;
            }
        }

        /// <summary>
        /// Método auxiliar para determinar si un JsonElement representa un valor "success" verdadero.
        /// </summary>
        private bool IsSuccessValue(JsonElement element)
        {
            try
            {
                // Intentar como booleano
                if (element.ValueKind == JsonValueKind.True)
                    return true;
                
                if (element.ValueKind == JsonValueKind.False)
                    return false;

                // Intentar como string
                if (element.ValueKind == JsonValueKind.String)
                {
                    var stringValue = element.GetString()?.ToLower();
                    return stringValue == "true" || stringValue == "1" || stringValue == "success";
                }

                // Intentar como número
                if (element.ValueKind == JsonValueKind.Number)
                {
                    return element.GetInt32() > 0;
                }

                return false;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Método auxiliar para parsear la respuesta de login desde un elemento JSON.
        /// </summary>
        private LoginResponseDto ParseLoginResponse(JsonElement dataElement)
        {
            try
            {
                // Extraer token
                var token = dataElement.TryGetProperty("token", out var tokenElement) 
                    ? tokenElement.GetString() 
                    : null;

                // Extraer fecha de expiración
                var expiresAtString = dataElement.TryGetProperty("expires_at", out var expiresElement) 
                    ? expiresElement.GetString() 
                    : null;
                DateTime.TryParse(expiresAtString, out var expiresAt);

                // Extraer datos del usuario
                var userElement = dataElement.TryGetProperty("user", out var userElementProp) 
                    ? userElementProp 
                    : dataElement; // Si no hay 'user', usar el elemento raíz

                var userId = userElement.TryGetProperty("id", out var idElement) 
                    ? idElement.GetInt32() 
                    : 0;

                var userEmail = userElement.TryGetProperty("email", out var emailElement) 
                    ? emailElement.GetString() 
                    : "";

                var roleId = userElement.TryGetProperty("role_id", out var roleElement) 
                    ? roleElement.GetInt32() 
                    : 1;

                // Si no tenemos token, considerar como fallo
                if (string.IsNullOrEmpty(token))
                {
                    return LoginResponseDto.Failure("Token no encontrado en la respuesta");
                }

                // Crear DTO de sesión
                var sessionDto = new UserSessionDto
                {
                    SessionId = Guid.NewGuid().ToString(),
                    UserId = userId,
                    UserEmail = userEmail ?? string.Empty,
                    UserRut = string.Empty, // No viene en la respuesta por ahora
                    RoleId = roleId,
                    CreatedAt = DateTime.UtcNow,
                    ExpiresAt = expiresAt,
                    IsActive = true
                };

                return LoginResponseDto.Success(
                    token,
                    expiresAt,
                    sessionDto.SessionId,
                    sessionDto
                );
            }
            catch (Exception ex)
            {
                return LoginResponseDto.Failure($"Error al parsear respuesta: {ex.Message}");
            }
        }

        #endregion
    }
}