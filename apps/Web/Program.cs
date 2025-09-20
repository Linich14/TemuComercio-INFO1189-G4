using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Web;
using Application.Services;
using Application.Interfaces;

// Configuración inicial de la aplicación Blazor WebAssembly
var builder = WebAssemblyHostBuilder.CreateDefault(args);

// Registrar componentes raíz de la aplicación
builder.RootComponents.Add(typeof(Web.App), "#app");                    // Componente principal en el div con id "app"
builder.RootComponents.Add<HeadOutlet>("head::after");     // Gestión del <head> del documento

// SERVICIOS DE INFRAESTRUCTURA
// HttpClient configurado para comunicación con el backend (cuando esté disponible)
// BaseAddress se configura automáticamente según el entorno (desarrollo/producción)
builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });

// INYECCIÓN DE DEPENDENCIAS - FRONTEND SIMPLIFICADO
// Configuración mínima para funcionamiento del frontend con simulación

// Servicio de Autenticación (con simulación incluida para demo)
builder.Services.AddScoped<IAuthenticationService, AuthenticationService>();

// Construir y ejecutar la aplicación
await builder.Build().RunAsync();
