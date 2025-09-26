using Microsoft.JSInterop;

namespace Application.Services
{
    /// <summary>
    /// Servicio para manejar el estado de autenticación en el frontend.
    /// Gestiona tokens, localStorage y validación de sesiones de manera centralizada.
    /// </summary>
    public class AuthenticationStateService
    {
        private readonly IJSRuntime _jsRuntime;
        
        public AuthenticationStateService(IJSRuntime jsRuntime)
        {
            _jsRuntime = jsRuntime;
        }

        /// <summary>
        /// Obtiene el token de autenticación almacenado en localStorage.
        /// </summary>
        public async Task<string?> GetTokenAsync()
        {
            try
            {
                return await _jsRuntime.InvokeAsync<string?>("localStorage.getItem", "authToken");
            }
            catch
            {
                return null;
            }
        }

        /// <summary>
        /// Verifica si el token ha expirado según la fecha almacenada.
        /// </summary>
        public async Task<bool> IsTokenExpiredAsync()
        {
            try
            {
                var expiryString = await _jsRuntime.InvokeAsync<string?>("localStorage.getItem", "tokenExpiresAt");
                
                if (string.IsNullOrWhiteSpace(expiryString))
                    return true;

                if (DateTime.TryParse(expiryString, out var expiryDate))
                {
                    return DateTime.UtcNow >= expiryDate;
                }

                return true;
            }
            catch
            {
                return true;
            }
        }

        /// <summary>
        /// Verifica si el usuario está autenticado (tiene token válido no expirado).
        /// </summary>
        public async Task<bool> IsAuthenticatedAsync()
        {
            var token = await GetTokenAsync();
            if (string.IsNullOrWhiteSpace(token))
                return false;

            return !await IsTokenExpiredAsync();
        }

        /// <summary>
        /// Limpia todos los datos de autenticación del localStorage.
        /// </summary>
        public async Task ClearAuthenticationAsync()
        {
            try
            {
                await _jsRuntime.InvokeVoidAsync("localStorage.removeItem", "authToken");
                await _jsRuntime.InvokeVoidAsync("localStorage.removeItem", "tokenExpiresAt");
                await _jsRuntime.InvokeVoidAsync("localStorage.removeItem", "userId");
                await _jsRuntime.InvokeVoidAsync("localStorage.removeItem", "userEmail");
                await _jsRuntime.InvokeVoidAsync("localStorage.removeItem", "userRoleId");
            }
            catch
            {
                // Ignorar errores al limpiar localStorage
            }
        }

        /// <summary>
        /// Obtiene el email del usuario almacenado.
        /// </summary>
        public async Task<string?> GetUserEmailAsync()
        {
            try
            {
                return await _jsRuntime.InvokeAsync<string?>("localStorage.getItem", "userEmail");
            }
            catch
            {
                return null;
            }
        }

        /// <summary>
        /// Obtiene el ID del rol del usuario almacenado.
        /// </summary>
        public async Task<int?> GetUserRoleIdAsync()
        {
            try
            {
                var roleIdString = await _jsRuntime.InvokeAsync<string?>("localStorage.getItem", "userRoleId");
                if (int.TryParse(roleIdString, out var roleId))
                {
                    return roleId;
                }
                return null;
            }
            catch
            {
                return null;
            }
        }
    }
}