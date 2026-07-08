from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config.database import get_engine
from schemas.administracion import RolCreate, RolUpdate, UsuarioCreate, UsuarioUpdate
from utils.exceptions import DatabaseError


def _ejecutar_listado(nombre_procedimiento: str, parametros: dict[str, Any]) -> list[dict]:
    """Ejecuta un procedimiento almacenado de consulta y retorna diccionarios."""
    try:
        placeholders = ", ".join(f":{nombre}" for nombre in parametros)
        sentencia = text(f"EXEC {nombre_procedimiento} {placeholders}")

        with get_engine().connect() as connection:
            result = connection.execute(sentencia, parametros)
            return [dict(row) for row in result.mappings().all()]
    except SQLAlchemyError as exc:
        raise DatabaseError(f"Error al ejecutar {nombre_procedimiento}: {exc}") from exc


def _ejecutar_comando(nombre_procedimiento: str, parametros: dict[str, Any]) -> None:
    """Ejecuta un procedimiento almacenado de escritura dentro de una transaccion."""
    try:
        placeholders = ", ".join(f":{nombre}" for nombre in parametros)
        sentencia = text(f"EXEC {nombre_procedimiento} {placeholders}")

        with get_engine().begin() as connection:
            connection.execute(sentencia, parametros)
    except SQLAlchemyError as exc:
        raise DatabaseError(f"Error al ejecutar {nombre_procedimiento}: {exc}") from exc


def listar_usuarios(usuario_id: int | None, incluir_inactivos: bool) -> list[dict]:
    """Consulta usuarios registrados en la aplicacion."""
    return _ejecutar_listado(
        "dbo.USP_AppUsuarioListar",
        {
            "usuario_id": usuario_id,
            "incluir_inactivos": incluir_inactivos,
        },
    )


def crear_usuario(usuario: UsuarioCreate, password_hash: str) -> None:
    """Crea un usuario mediante procedimiento almacenado."""
    _ejecutar_comando(
        "dbo.USP_AppUsuarioCrear",
        {
            "usuario": usuario.Usuario,
            "password_hash": password_hash,
            "nombre_completo": usuario.NombreCompleto,
            "correo": usuario.Correo,
            "activo": usuario.Activo,
        },
    )


def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate) -> None:
    """Actualiza los datos editables de un usuario."""
    _ejecutar_comando(
        "dbo.USP_AppUsuarioActualizar",
        {
            "usuario_id": usuario_id,
            "usuario": usuario.Usuario,
            "nombre_completo": usuario.NombreCompleto,
            "correo": usuario.Correo,
            "activo": usuario.Activo,
        },
    )


def eliminar_usuario(usuario_id: int) -> None:
    """Realiza eliminacion logica de usuario."""
    _ejecutar_comando(
        "dbo.USP_AppUsuarioEliminarLogico",
        {"usuario_id": usuario_id},
    )


def reiniciar_password(usuario_id: int, password_hash: str) -> None:
    """Actualiza el hash de contrasena de un usuario."""
    _ejecutar_comando(
        "dbo.USP_AppUsuarioReiniciarPassword",
        {
            "usuario_id": usuario_id,
            "password_hash": password_hash,
        },
    )


def listar_roles(rol_id: int | None) -> list[dict]:
    """Consulta roles de la aplicacion."""
    return _ejecutar_listado(
        "dbo.USP_AppRolListar",
        {"rol_id": rol_id},
    )


def crear_rol(rol: RolCreate) -> None:
    """Crea un rol mediante procedimiento almacenado."""
    _ejecutar_comando(
        "dbo.USP_AppRolCrear",
        {"nombre_rol": rol.NombreRol},
    )


def actualizar_rol(rol_id: int, rol: RolUpdate) -> None:
    """Actualiza el nombre de un rol."""
    _ejecutar_comando(
        "dbo.USP_AppRolActualizar",
        {
            "rol_id": rol_id,
            "nombre_rol": rol.NombreRol,
        },
    )


def eliminar_rol(rol_id: int) -> None:
    """Elimina un rol si no tiene usuarios asociados."""
    _ejecutar_comando(
        "dbo.USP_AppRolEliminar",
        {"rol_id": rol_id},
    )


def asignar_roles(usuario_id: int, roles_id: list[int]) -> None:
    """Reemplaza los roles de un usuario usando una lista CSV para SQL Server."""
    roles_csv = ",".join(str(rol_id) for rol_id in roles_id)
    _ejecutar_comando(
        "dbo.USP_AppUsuarioAsignarRoles",
        {
            "usuario_id": usuario_id,
            "roles_csv": roles_csv,
        },
    )
