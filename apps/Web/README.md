# TemuComercio - Frontend (Blazor WebAssembly)

## 📋 Descripción del Proyecto

Este es el frontend de TemuComercio desarrollado en **Blazor WebAssembly** siguiendo principios de **Clean Architecture**. El proyecto está diseñado para trabajar de manera independiente del backend, utilizando servicios de API para la comunicación.

## 🏗️ Arquitectura del Frontend

### Estructura de Carpetas

```
📁 Web/
├── 📁 Application/
│   ├── 📁 DTOs/                    # Data Transfer Objects
│   │   ├── LoginRequestDto.cs      # Datos para solicitud de login
│   │   ├── LoginResponseDto.cs     # Respuesta del proceso de login
│   │   └── UserSessionDto.cs       # Datos de sesión del usuario
│   └── 📁 Services/
│       └── AuthApiService.cs       # Servicio para comunicación con backend
│  📁 WebUI/
│  ├── 📁 Components/
│  ├── 📁 Authentication/          
│  │   │   ├── LoginForm.razor         
│  │   │   └── RecoverPasswordForm.razor 
│  │   └── 📁 Common/                  
│  ├── 📁 Pages/
│  │   ├── 📁 Authentication/          
│  │   │   ├── Login.razor             
│  │   │   ├── RecoverPassword.razor   
│  │   │   └── WelcomeScreen.razor     
│  │   ├── 📁 Dashboard/               
│  │   │   └── Dashboard.razor         
│  │   └── Home.razor                  
│  └── 📁 Shared/
│  ├── AuthLayout.razor
   └── MainLayout.razor     
```

### Separación de Responsabilidades

#### ✅ **Frontend (Este proyecto)**
- **Application/DTOs**: Objetos para transferir datos con el backend
- **Application/Services**: Servicios para comunicación con APIs
- **WebUI**: Interfaz de usuario (páginas y componentes)
- **Validaciones de UI**: Formato de RUT, longitud de contraseñas
- **Gestión de estado local**: localStorage para sessiones


## 🚀 Configuración y Ejecución

### Prerrequisitos
- .NET 8.0 SDK
- Node.js (para Tailwind CSS)

### Pasos para ejecutar

1. **Restaurar dependencias**
   ```powershell
   dotnet restore
   ```

2. **Compilar Tailwind CSS**
   ```powershell
   npm install
   npm run build:css
   ```

3. **Ejecutar la aplicación**
   ```powershell
   dotnet run
   ```

4. **Abrir en el navegador**
   ```
   https://localhost:5001
   ```


## 🎨 Diseño y Estilos

### Tailwind CSS

El proyecto utiliza **Tailwind CSS** para todos los estilos:

- **Configuración**: `tailwind.config.js`
- **Compilación**: `npm run build:css`
- **Archivo generado**: `wwwroot/css/app.css`

### Layouts Específicos

- **AuthLayout**: Para login, welcome y recuperar contraseña
- **MainLayout**: Para páginas internas (dashboard, etc.)



## 🔧 Mantenimiento

### Actualizar Dependencias

```powershell
dotnet list package --outdated
dotnet add package PackageName --version x.x.x
```

### Regenerar CSS

```powershell
npm run build:css
```

### Limpiar Build

```powershell
dotnet clean
dotnet build
```

