"""
Auth views for login endpoint.
Handles user authentication with session tokens.
"""
import json
import uuid
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import hashlib
import re


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def login_view(request):
    """
    Endpoint para login de usuario con tokens de sesión manuales.

    POST /api/auth/login/
    Content-Type: application/json

    Body:
    {
        "email": "admin@temucomercio.cl",
        "password": "Administrador123!",
        "remember_me": true
    }

    Response 200:
    {
        "success": true,
        "message": "Inicio de sesión exitoso",
        "data": {
            "token": "550e8400-e29b-41d4-a716-446655440000",
            "expires_at": "2025-10-22T14:30:00Z",
            "user": {
                "id": 123,
                "email": "admin@temucomercio.cl",
                "role_id": 1
            }
        }
    }
    """
    if request.method == 'OPTIONS':
        return JsonResponse({}, status=200)

    try:
        # Parsear datos JSON
        data = json.loads(request.body)

        # Extraer campos
        email = data.get('email', '').strip()
        password = data.get('password', '')
        remember_me = data.get('remember_me', False)

        # Validaciones básicas
        errors = []

        if not email:
            errors.append("Email es requerido")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append("Formato de email inválido")

        if not password:
            errors.append("Contraseña es requerida")

        if errors:
            return JsonResponse({
                "success": False,
                "message": "Datos inválidos",
                "errors": errors
            }, status=400)

        # Buscar usuario por email
        from core_models.models import UsuarioModel
        try:
            usuario = UsuarioModel.objects.get(usua_email=email.lower())
        except ObjectDoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Credenciales incorrectas",
                "errors": ["Email o contraseña inválidos"]
            }, status=401)

        # Verificar que el usuario esté activo
        if usuario.usua_estado != 1:
            return JsonResponse({
                "success": False,
                "message": "Credenciales incorrectas",
                "errors": ["Cuenta desactivada"]
            }, status=401)

        # Verificar contraseña (hash SHA-256)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if usuario.usua_pass != hashed_password:
            return JsonResponse({
                "success": False,
                "message": "Credenciales incorrectas",
                "errors": ["Email o contraseña inválidos"]
            }, status=401)

        # Invalidar tokens existentes del usuario
        from core_models.models import SesionTokenModel
        SesionTokenModel.objects.filter(
            usua_id=usuario,
            token_activo=True
        ).update(token_activo=False)

        # Crear nuevo token
        token_valor = str(uuid.uuid4())

        # Calcular fecha de expiración
        if remember_me:
            expires_at = timezone.now() + timedelta(days=30)
        else:
            expires_at = timezone.now() + timedelta(days=1)

        # Crear registro en Sesion_Token
        nuevo_token = SesionTokenModel.objects.create(
            usua_id=usuario,
            token_valor=token_valor,
            token_expira_en=expires_at,
            token_activo=True
        )

        # Preparar respuesta
        response_data = {
            "success": True,
            "message": "Inicio de sesión exitoso",
            "data": {
                "token": token_valor,
                "expires_at": expires_at.isoformat(),
                "user": {
                    "id": usuario.usua_id,
                    "email": usuario.usua_email,
                    "role_id": usuario.rous_id.rous_id if usuario.rous_id else None
                }
            }
        }

        # Logging para debugging
        print(f"🔐 LOGIN SUCCESS: User {usuario.usua_email} (ID: {usuario.usua_id}) logged in")
        print(f"📝 Response data: {response_data}")

        response = JsonResponse(response_data, status=200)

        # Headers de debug para frontend
        response['X-Debug-Token'] = token_valor[:8] + "..."
        response['X-Debug-User-ID'] = str(usuario.usua_id)
        response['X-Debug-Role-ID'] = str(usuario.rous_id.rous_id if usuario.rous_id else 'None')

        return response

    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "message": "Datos inválidos",
            "errors": ["JSON malformado"]
        }, status=400)

    except Exception as e:
        # Log del error para debugging
        print(f"Error en login: {str(e)}")
        return JsonResponse({
            "success": False,
            "message": "Error interno del servidor",
            "errors": ["Error interno del servidor"]
        }, status=500)


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def logout_view(request):
    """
    Endpoint para cerrar sesión invalidando el token.

    POST /api/auth/logout/
    Headers: Authorization: Bearer <token>
    Content-Type: application/json

    Response 200:
    {
        "success": true,
        "message": "Sesión cerrada exitosamente"
    }
    """
    if request.method == 'OPTIONS':
        return JsonResponse({}, status=200)

    try:
        # Obtener token del header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({
                "success": False,
                "message": "Token requerido",
                "errors": ["Header Authorization con Bearer token requerido"]
            }, status=401)

        token = auth_header.replace('Bearer ', '').strip()

        if not token:
            return JsonResponse({
                "success": False,
                "message": "Token requerido",
                "errors": ["Token no puede estar vacío"]
            }, status=401)

        # Buscar e invalidar el token
        from core_models.models import SesionTokenModel
        try:
            token_obj = SesionTokenModel.objects.get(
                token_valor=token,
                token_activo=True
            )

            # Verificar si no ha expirado
            if token_obj.is_expired:
                return JsonResponse({
                    "success": False,
                    "message": "Token expirado",
                    "errors": ["El token ya ha expirado"]
                }, status=401)

            # Invalidar el token
            token_obj.token_activo = False
            token_obj.save()

            return JsonResponse({
                "success": True,
                "message": "Sesión cerrada exitosamente"
            }, status=200)

        except SesionTokenModel.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Token inválido",
                "errors": ["Token no encontrado o ya invalidado"]
            }, status=401)

    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "message": "Datos inválidos",
            "errors": ["JSON malformado"]
        }, status=400)

    except Exception as e:
        # Log del error para debugging
        print(f"Error en logout: {str(e)}")
        return JsonResponse({
            "success": False,
            "message": "Error interno del servidor",
            "errors": ["Error interno del servidor"]
        }, status=500)


@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def verify_token_view(request):
    """
    Endpoint para verificar si un token es válido.

    GET /api/auth/verify/
    Headers: Authorization: Bearer <token>

    Response 200:
    {
        "success": true,
        "message": "Token válido",
        "data": {
            "user": {
                "id": 123,
                "email": "admin@temucomercio.cl",
                "role_id": 1
            },
            "expires_at": "2025-10-22T14:30:00Z"
        }
    }
    """
    if request.method == 'OPTIONS':
        return JsonResponse({}, status=200)

    try:
        # Obtener token del header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({
                "success": False,
                "message": "Token requerido",
                "errors": ["Header Authorization con Bearer token requerido"]
            }, status=401)

        token = auth_header.replace('Bearer ', '').strip()

        if not token:
            return JsonResponse({
                "success": False,
                "message": "Token requerido",
                "errors": ["Token no puede estar vacío"]
            }, status=401)

        # Buscar el token
        from core_models.models import SesionTokenModel
        try:
            token_obj = SesionTokenModel.objects.select_related('usua_id').get(
                token_valor=token,
                token_activo=True
            )

            # Verificar si no ha expirado
            if token_obj.is_expired:
                return JsonResponse({
                    "success": False,
                    "message": "Token expirado",
                    "errors": ["El token ha expirado"]
                }, status=401)

            # Token válido, devolver información del usuario
            usuario = token_obj.usua_id
            return JsonResponse({
                "success": True,
                "message": "Token válido",
                "data": {
                    "user": {
                        "id": usuario.usua_id,
                        "email": usuario.usua_email,
                        "role_id": usuario.rous_id.rous_id if usuario.rous_id else None
                    },
                    "expires_at": token_obj.token_expira_en.isoformat()
                }
            }, status=200)

        except SesionTokenModel.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Token inválido",
                "errors": ["Token no encontrado o invalidado"]
            }, status=401)

    except Exception as e:
        # Log del error para debugging
        print(f"Error en verify_token: {str(e)}")
        return JsonResponse({
            "success": False,
            "message": "Error interno del servidor",
            "errors": ["Error interno del servidor"]
        }, status=500)