# Django REST API Project - Clean Architecture

Este proyecto está basado en Django y Django REST Framework, siguiendo los principios de **Clean Architecture**, **Arquitectura Hexagonal** y **SOLID**.

## Arquitectura

### Estructura de Carpetas

```
src/
├── core/                           # Núcleo de la aplicación
│   ├── domain/                     # Capa de Dominio
│   │   ├── entities/              # Entidades de negocio
│   │   ├── repositories/          # Interfaces de repositorios
│   │   └── services/              # Servicios de dominio
│   └── application/               # Capa de Aplicación
│       ├── use_cases/             # Casos de uso
│       └── dto/                   # Data Transfer Objects
├── infrastructure/               # Capa de Infraestructura
│   ├── repositories/             # Implementaciones de repositorios
│   ├── external_services/        # Servicios externos
│   └── di/                       # Inyección de dependencias
└── interfaces/                   # Capa de Interfaces
    └── api/                      # API REST
        ├── views/                # Controladores
        └── serializers/          # Serializadores
```

### Principios Aplicados

#### Clean Architecture
- **Capas bien definidas**: Domain, Application, Infrastructure, Interfaces
- **Dependencias hacia el centro**: Las capas externas dependen de las internas
- **Inversión de dependencias**: Se usan interfaces para desacoplar capas

#### Arquitectura Hexagonal
- **Puertos**: Interfaces que definen contratos (ej: `ProductRepository`)
- **Adaptadores**: Implementaciones concretas (ej: `DjangoProductRepository`)
- **Núcleo aislado**: La lógica de negocio no depende de frameworks

#### SOLID
1. **Single Responsibility**: Cada clase tiene una única responsabilidad
2. **Open/Closed**: Extensible sin modificar código existente
3. **Liskov Substitution**: Las implementaciones pueden sustituir interfaces
4. **Interface Segregation**: Interfaces específicas y pequeñas
5. **Dependency Inversion**: Dependencias abstraídas mediante interfaces

## Comandos Útiles

### Desarrollo
```powershell
# Activar entorno virtual
.venv\Scripts\Activate.ps1

# Verificar configuración de Supabase
& .venv\Scripts\python.exe manage.py test_supabase

# Iniciar servidor de desarrollo
& .venv\Scripts\python.exe manage.py runserver

# Crear migraciones
& .venv\Scripts\python.exe manage.py makemigrations

# Aplicar migraciones
& .venv\Scripts\python.exe manage.py migrate
```

### API Endpoints de Ejemplo

#### Productos
- `GET /api/products/` - Listar todos los productos
- `POST /api/products/` - Crear nuevo producto
- `GET /api/products/{id}/` - Obtener producto por ID
- `PATCH /api/products/{id}/stock/` - Actualizar stock del producto


## Configuración de Entornos

El proyecto usa configuraciones separadas siguiendo el principio Open/Closed:

- `config/settings/base.py` - Configuración base
- `config/settings/development.py` - Configuración de desarrollo
- `config/settings/production.py` - Configuración de producción

### Variables de entorno:

1. **Copiar el archivo de ejemplo:**
```powershell
cp .env.example .env
```

2. **Configurar variables en `.env`:**
```bash
SECRET_KEY=tu-secret-key-super-segura-nueva
DEBUG=True
DJANGO_SETTINGS_MODULE=config.settings.development
```

⚠️ **IMPORTANTE**: El archivo `.env` contiene información sensible y NO debe subirse a git.


## Dependencias Principales

- **Django**: Framework web
- **djangorestframework**: Para APIs REST
- **python-dotenv**: Manejo de variables de entorno
- **psycopg2-binary**: Adaptador de PostgreSQL para Django
- **supabase**: Cliente oficial de Supabase
- **Arquitectura personalizada**: Clean Architecture + Hexagonal + SOLID

## Base de Datos - Supabase

El proyecto está configurado para usar **Supabase** (PostgreSQL) como base de datos principal:

### Configuración de Supabase:

1. **Crear proyecto en Supabase:**
   - Ve a [https://app.supabase.com](https://app.supabase.com)
   - Crea un nuevo proyecto
   - Anota la URL del proyecto y las claves de API

2. **Obtener credenciales de base de datos:**
   - Ve a Settings > Database
   - Copia: Host, Database name, Username, Password, Port

3. **Configurar variables de entorno:**
```bash
# Supabase API
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu-anon-key
SUPABASE_SERVICE_ROLE_KEY=tu-service-role-key

# Supabase Database
SUPABASE_DB_HOST=db.tu-proyecto.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=tu-password
SUPABASE_DB_PORT=5432
```

4. **Verificar configuración:**
```powershell
& .venv\Scripts\python.exe manage.py test_supabase
```

5. **Aplicar migraciones:**
```powershell
& .venv\Scripts\python.exe manage.py migrate
```

### Fallback a SQLite:
Si no se configuran las credenciales de Supabase, el proyecto automáticamente usa SQLite para desarrollo local.


## Inyección de Dependencias

El proyecto incluye un contenedor simple de dependencias en `src/infrastructure/di/container.py` que gestiona las implementaciones de interfaces siguiendo el principio de Inversión de Dependencias.
