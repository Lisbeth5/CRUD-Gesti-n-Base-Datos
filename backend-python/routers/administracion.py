from fastapi import APIRouter, Query

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
from services import administracion_service


usuarios_router = APIRouter(prefix="/api/usuarios", tags=["Administracion - Usuarios"])
roles_router = APIRouter(prefix="/api/roles", tags=["Administracion - Roles"])


@usuarios_router.get("", response_model=list[UsuarioResponse])
def listar_usuarios(
    usuario_id: int | None = Query(default=None, ge=1),
    incluir_inactivos: bool = Query(default=False),
) -> list[UsuarioResponse]:
    """Lista usuarios de la aplicacion con filtros opcionales."""
    return administracion_service.listar_usuarios(usuario_id, incluir_inactivos)


@usuarios_router.post("", response_model=MensajeResponse)
def crear_usuario(usuario: UsuarioCreate) -> MensajeResponse:
    """Registra un usuario con contrasena hasheada en el servicio."""
    return administracion_service.crear_usuario(usuario)


@usuarios_router.put("/{usuario_id}", response_model=MensajeResponse)
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate) -> MensajeResponse:
    """Actualiza datos generales de un usuario."""
    return administracion_service.actualizar_usuario(usuario_id, usuario)


@usuarios_router.delete("/{usuario_id}", response_model=MensajeResponse)
def eliminar_usuario(usuario_id: int) -> MensajeResponse:
    """Ejecuta eliminacion logica de un usuario."""
    return administracion_service.eliminar_usuario(usuario_id)


@usuarios_router.post("/reiniciar-password", response_model=MensajeResponse)
def reiniciar_password(solicitud: ReiniciarPasswordRequest) -> MensajeResponse:
    """Reinicia la contrasena de un usuario."""
    return administracion_service.reiniciar_password(solicitud)


@usuarios_router.post("/asignar-roles", response_model=MensajeResponse)
def asignar_roles(solicitud: AsignarRolesRequest) -> MensajeResponse:
    """Reemplaza los roles asignados a un usuario."""
    return administracion_service.asignar_roles(solicitud)


@roles_router.get("", response_model=list[RolResponse])
def listar_roles(rol_id: int | None = Query(default=None, ge=1)) -> list[RolResponse]:
    """Lista roles de la aplicacion."""
    return administracion_service.listar_roles(rol_id)


@roles_router.post("", response_model=MensajeResponse)
def crear_rol(rol: RolCreate) -> MensajeResponse:
    """Crea un rol de aplicacion."""
    return administracion_service.crear_rol(rol)


@roles_router.put("/{rol_id}", response_model=MensajeResponse)
def actualizar_rol(rol_id: int, rol: RolUpdate) -> MensajeResponse:
    """Actualiza un rol de aplicacion."""
    return administracion_service.actualizar_rol(rol_id, rol)


@roles_router.delete("/{rol_id}", response_model=MensajeResponse)
def eliminar_rol(rol_id: int) -> MensajeResponse:
    """Elimina un rol si no tiene usuarios asociados."""
    return administracion_service.eliminar_rol(rol_id)
