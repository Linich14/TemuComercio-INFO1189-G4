# TemuComercio - Frontend (Blazor WebAssembly)

## 📋 Descripción del Proyecto

Este es el frontend de TemuComercio para Web desarrollado en **Blazor WebAssembly** siguiendo principios de **Clean Architecture**. El proyecto está diseñado para trabajar de manera independiente del backend, utilizando servicios de API para la comunicación.


## 🏗️ Arquitectura Frontend Implementada

Este proyecto frontend sigue los principios de **Clean Architecture**, **Arquitectura Hexagonal** y **SOLID**, proporcionando una base sólida, mantenible y escalable.

### 📁 Estructura de Capas

```
📁 Web/
├── 📁 Domain/                          # ⭐ CAPA DE DOMINIO
│   ├── 📁 Entities/                    # Entidades de negocio
│   ├── 📁 ValueObjects/                # Objetos de valor
│   └── 📁 Services/                    # Interfaces de servicios de dominio
│
├── 📁 Application/                     # ⭐ CAPA DE APLICACIÓN
│   ├── 📁 DTOs/                        # Objetos de transferencia de datos
│   ├── 📁 Interfaces/                  # Puertos (Hexagonal Architecture)
│   └── 📁 Validators/                  # Validadores de reglas de negocio
│
├── 📁 Infrastructure/                  # ⭐ CAPA DE INFRAESTRUCTURA
│   ├── 📁 Services/                    # Implementaciones de servicios
│   └── 📁 Adapters/                    # Adaptadores externos
│
└── 📁 WebUI/                          # ⭐ CAPA DE PRESENTACIÓN
    ├── 📁 Components/                  # Componentes reutilizables
    │   └── 📁 Authentication/
    ├── 📁 Pages/                       # Páginas de la aplicación
    │   ├── 📁 Authentication/
    │   ├── 📁 Dashboard/
    │   └── Home.razor
    └── 📁 Shared/                      # Layouts compartidos

```

---

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


## 🔧 Mantenimiento


### Regenerar CSS

```powershell
npm run build:css
```

### Limpiar Build

```powershell
dotnet clean
dotnet build
```

