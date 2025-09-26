using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Web;
using Application.Interfaces;
using Domain.Services;
using Infrastructure.Services;

// Configuración inicial de la aplicación Blazor WebAssembly
var builder = WebAssemblyHostBuilder.CreateDefault(args);

// Registrar componentes raíz de la aplicación
builder.RootComponents.Add(typeof(Web.App), "#app");                    // Componente principal en el div con id "app"
builder.RootComponents.Add<HeadOutlet>("head::after");     // Gestión del <head> del documento

// SERVICIOS DE INFRAESTRUCTURA
// HttpClient configurado para comunicación con el backend Django
builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri("http://127.0.0.1:8000/") });

// INYECCIÓN DE DEPENDENCIAS - CLEAN ARCHITECTURE
// Configuración siguiendo principios de Clean Architecture y SOLID

// Domain Services - Lógica de negocio pura
builder.Services.AddScoped<IAuthenticationDomainService, AuthenticationDomainService>();

// Application Services - Casos de uso y orquestación
builder.Services.AddScoped<IAuthenticationService, Infrastructure.Services.AuthenticationService>();
builder.Services.AddScoped<Application.Services.AuthenticationStateService>();

// Construir y ejecutar la aplicación
await builder.Build().RunAsync();
