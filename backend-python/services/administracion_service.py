from repositories import administracion_repository
from schemas.administracion import (
    AsignarRolesRequest,
    MensajeResponse,
    ReiniciarPasswordRequest,
    RolCreate,
    RolResponse,
    RolUpdate,
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)
from utils.exceptions import AppError
from utils.security import generar_password_hash


def listar_usuarios(usuario_id: int | None, incluir_inactivos: bool) -> list[UsuarioResponse]:
    """Obtiene usuarios y valida la respuesta publica."""
    filas = administracion_repository.listar_usuarios(usuario_id, incluir_inactivos)
    return [UsuarioResponse.model_validate(fila) for fila in filas]


def crear_usuario(usuario: UsuarioCreate) -> MensajeResponse:
    """Registra un usuario con contrasena hasheada."""
    try:
        password_hash = generar_password_hash(usuario.Password)
    except ValueError as exc:
        raise AppError(str(exc)) from exc

    administracion_repository.crear_usuario(usuario, password_hash)
    return MensajeResponse(mensaje="Usuario creado exitosamente")


def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate) -> MensajeResponse:
    """Actualiza datos generales de usuario."""
    administracion_repository.actualizar_usuario(usuario_id, usuario)
    return MensajeResponse(mensaje=f"Usuario {usuario_id} actualizado exitosamente")


def eliminar_usuario(usuario_id: int) -> MensajeResponse:
    """Desactiva un usuario sin borrar su historial."""
    administracion_repository.eliminar_usuario(usuario_id)
    return MensajeResponse(mensaje=f"Usuario {usuario_id} desactivado exitosamente")


def reiniciar_password(solicitud: ReiniciarPasswordRequest) -> MensajeResponse:
    """Genera un nuevo hash para la contrasena recibida."""
    try:
        password_hash = generar_password_hash(solicitud.NuevaPassword)
    except ValueError as exc:
        raise AppError(str(exc)) from exc

    administracion_repository.reiniciar_password(solicitud.UsuarioID, password_hash)
    return MensajeResponse(mensaje="Contrasena reiniciada exitosamente")


def listar_roles(rol_id: int | None) -> list[RolResponse]:
    """Obtiene roles y valida la respuesta publica."""
    filas = administracion_repository.listar_roles(rol_id)
    return [RolResponse.model_validate(fila) for fila in filas]


def crear_rol(rol: RolCreate) -> MensajeResponse:
    """Crea un rol de aplicacion."""
    administracion_repository.crear_rol(rol)
    return MensajeResponse(mensaje="Rol creado exitosamente")


def actualizar_rol(rol_id: int, rol: RolUpdate) -> MensajeResponse:
    """Actualiza un rol de aplicacion."""
    administracion_repository.actualizar_rol(rol_id, rol)
    return MensajeResponse(mensaje=f"Rol {rol_id} actualizado exitosamente")


def eliminar_rol(rol_id: int) -> MensajeResponse:
    """Elimina un rol si no esta asociado a usuarios."""
    administracion_repository.eliminar_rol(rol_id)
    return MensajeResponse(mensaje=f"Rol {rol_id} eliminado exitosamente")


def asignar_roles(solicitud: AsignarRolesRequest) -> MensajeResponse:
    """Reemplaza los roles de un usuario."""
    roles_unicos = sorted(set(solicitud.RolesID))
    if any(rol_id <= 0 for rol_id in roles_unicos):
        raise AppError("Todos los identificadores de rol deben ser mayores a cero.")

    administracion_repository.asignar_roles(solicitud.UsuarioID, roles_unicos)
    return MensajeResponse(mensaje="Roles asignados exitosamente")
