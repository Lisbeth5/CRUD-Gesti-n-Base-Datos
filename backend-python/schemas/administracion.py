from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


def to_camel_case(field_name: str) -> str:
    """Convierte nombres PascalCase a camelCase para aceptar JSON de Blazor."""
    return field_name[0].lower() + field_name[1:] if field_name else field_name


class AdministracionBaseModel(BaseModel):
    """Modelo base que acepta propiedades PascalCase y camelCase."""

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel_case)


class UsuarioCreate(AdministracionBaseModel):
    """Datos requeridos para registrar un usuario de la aplicacion."""

    Usuario: str = Field(..., min_length=3, max_length=50)
    Password: str = Field(..., min_length=8, max_length=72)
    NombreCompleto: str = Field(..., min_length=3, max_length=120)
    Correo: str = Field(..., max_length=150)
    Activo: bool = True


class UsuarioUpdate(AdministracionBaseModel):
    """Datos editables de un usuario existente."""

    Usuario: str = Field(..., min_length=3, max_length=50)
    NombreCompleto: str = Field(..., min_length=3, max_length=120)
    Correo: str = Field(..., max_length=150)
    Activo: bool = True


class UsuarioResponse(AdministracionBaseModel):
    """Datos publicos de usuario retornados al frontend."""

    UsuarioID: int
    Usuario: str
    NombreCompleto: str
    Correo: str
    Activo: bool
    FechaCreacion: datetime
    Roles: str | None = None


class ReiniciarPasswordRequest(AdministracionBaseModel):
    """Solicitud para reiniciar la contrasena de un usuario."""

    UsuarioID: int = Field(..., ge=1)
    NuevaPassword: str = Field(..., min_length=8, max_length=72)


class RolCreate(AdministracionBaseModel):
    """Datos requeridos para crear un rol."""

    NombreRol: str = Field(..., min_length=3, max_length=50)


class RolUpdate(AdministracionBaseModel):
    """Datos requeridos para actualizar un rol."""

    NombreRol: str = Field(..., min_length=3, max_length=50)


class RolResponse(AdministracionBaseModel):
    """Datos publicos de rol retornados al frontend."""

    RolID: int
    NombreRol: str


class AsignarRolesRequest(AdministracionBaseModel):
    """Solicitud para reemplazar los roles asociados a un usuario."""

    UsuarioID: int = Field(..., ge=1)
    RolesID: list[int] = Field(default_factory=list)


class MensajeResponse(AdministracionBaseModel):
    """Respuesta simple para operaciones administrativas."""

    mensaje: str
